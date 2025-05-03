import os
import json
import csv
import signal
import sys
import time
from datetime import datetime
from kafka import KafkaConsumer
import gspread

# —————————————————————————————————————————————————————————————————————
# Google Sheets: konfiguracja gspread
# —————————————————————————————————————————————————————————————————————
CRED_PATH = 'creds.json'  # ścieżka do pliku serwisowego Google
gc = gspread.service_account(filename=CRED_PATH)
SHEET_NAME = 'source_looker'
SHEET_TAB  = 'Data'
sh = gc.open(SHEET_NAME)
worksheet = sh.worksheet(SHEET_TAB)

# —————————————————————————————————————————————————————————————————————
# Nagłówek arkusza i CSV z nowymi kolumnami
# —————————————————————————————————————————————————————————————————————
header = [
    'id', 'timestamp', 'store_id', 'region',
    'sales_channel', 'device_type', 'customer_id',
    'payment_method', 'nazwa_produktu', 'marka',
    'kategoria_produktu', 'ilosc', 'cena_netto',
    'wartosc_brutto', 'sprzedawca'
]

# Jeśli arkusz pusty, dodajemy nagłówek
if not worksheet.get_all_records():
    worksheet.append_row(header, value_input_option='USER_ENTERED')

# —————————————————————————————————————————————————————————————————————
# Graceful shutdown
# —————————————————————————————————————————————————————————————————————
running = True
def shutdown(signum, frame):
    global running
    print("\n[INFO] Zamykanie konsumenta…")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# —————————————————————————————————————————————————————————————————————
# KafkaConsumer
# —————————————————————————————————————————————————————————————————————
consumer = KafkaConsumer(
    'zamowienia_elektronika',
    bootstrap_servers='broker:9092',
    group_id='consumer_group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    key_deserializer=lambda x: x.decode('utf-8') if x else None,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# —————————————————————————————————————————————————————————————————————
# Przygotowanie CSV (rotacja dzienna)
# —————————————————————————————————————————————————————————————————————
output_dir = 'dane_dzienne'                 # nazwa folderu na pliki CSV
os.makedirs(output_dir, exist_ok=True)     # tworzymy folder, jeśli nie istnieje


today     = datetime.now().strftime("%Y-%m-%d")
file_path = os.path.join(output_dir, f"orders_{today}.csv") # budujemy ścieżkę: dane_dzienne/orders_YYYY-MM-DD.csv

csvfile = open(file_path, mode='w', newline='', encoding='utf-8')
writer  = csv.DictWriter(csvfile, fieldnames=header)
writer.writeheader()
print(f"[INFO] Zapisuję zamówienia do {file_path}")

try:
    while running:
        records = consumer.poll(timeout_ms=1000, max_records=20)
        sheet_batch = []
        for tp, msgs in records.items():
            for msg in msgs:
                order = msg.value

                # — Przygotowanie wiersza z wszystkimi polami —
                row = {col: order.get(col, '') for col in header}
                try:
                    writer.writerow(row)
                    csvfile.flush()
                    print(f"[SAVED CSV] order_id={row['id']}")
                except Exception as e:
                    print(f"[ERROR CSV] podczas zapisu zamówienia {row.get('id')}: {e}")

                # — Dodanie wiersza do paczki dla Google Sheets —
                sheet_batch.append([row[col] for col in header])

        # — Wysyłka paczki do arkusza —
        if sheet_batch:
            try:
                worksheet.append_rows(sheet_batch, value_input_option='USER_ENTERED')
                print(f"[SAVED SHEET] dodano {len(sheet_batch)} zamówień do arkusza")
            except Exception as e:
                print(f"[ERROR SHEET] przy dodawaniu do Sheets: {e}")

finally:
    consumer.close()
    csvfile.close()
    print("[INFO] Konsument zamknięty.")

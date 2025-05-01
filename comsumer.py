import json
import csv
import signal
import sys
from datetime import datetime
from kafka import KafkaConsumer

# —————————————————————————————————————————————————————————————————————
# Graceful shutdown
# —————————————————————————————————————————————————————————————————————
running = True

def shutdown(signum, frame):
    """Zamyka konsumenta przy SIGINT/SIGTERM"""
    global running
    print("\n[INFO] Zamykanie konsumenta…")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# —————————————————————————————————————————————————————————————————————
# Konfiguracja KafkaConsumer
# —————————————————————————————————————————————————————————————————————
consumer = KafkaConsumer(
    'zamowienia_elektronika',
    bootstrap_servers='localhost:9092',
    group_id='consumer_group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    key_deserializer=lambda x: x.decode('utf-8') if x else None,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# —————————————————————————————————————————————————————————————————————
# Przygotowanie CSV (rotacja dzienna)
# —————————————————————————————————————————————————————————————————————
today = datetime.now().strftime("%Y-%m-%d")
file_path = f"orders_{today}.csv"
fieldnames = [
    'id', 'timestamp', 'store_id', 'region', 'customer_id',
    'payment_method', 'nazwa_produktu', 'marka',
    'kategoria_produktu', 'ilosc', 'cena_netto', 'wartosc_brutto'
]

with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    print(f"[INFO] Zapisuję zamówienia do {file_path}")

    while running:
        # Pobranie partii wiadomości
        records = consumer.poll(timeout_ms=1000, max_records=20)
        for tp, msgs in records.items():
            for msg in msgs:
                order = msg.value
                # Wybór potrzebnych pól
                row = {fn: order.get(fn) for fn in fieldnames}
                try:
                    writer.writerow(row)
                    csvfile.flush()
                    print(f"[SAVED] order_id={row['id']}")
                except Exception as e:
                    print(f"[ERROR] podczas zapisu zamówienia {row.get('id')}: {e}")

    consumer.close()
    print("[INFO] Konsument zamknięty.")

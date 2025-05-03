import random
import uuid
import time
from datetime import datetime

# —————————————————————————————————————————————————————————————————————
# Konfiguracja danych syntetycznych
# —————————————————————————————————————————————————————————————————————

# Mapowanie regionów na odpowiadające im miasta
region_to_cities = {
    'Central':  ['Warszawa'],
    'Wschod':   ['Lublin', 'Terespol', 'Bialystok'],
    'Poludnie': ['Krakow', 'Katowice', 'Rzeszow', 'Czestochowa'],
    'Zachod':   ['Wroclaw', 'Poznan'],
    'Polnoc':   ['Gdansk', 'Gdynia', 'Bydgoszcz', 'Sopot', 'Szczecin']
}

# Dostępne kanały sprzedaży i powiązani sprzedawcy punktów stacjonarnych
sales_channels     = ['online', 'in_store']
store_salespersons = ['Ivan Petrov', 'Jan Kowalski', 'Kiryl Propapanko']
# Typy urządzeń dla kanału online
online_devices     = ['mobile', 'pc']

# Metody płatności
payment_methods    = ['cash', 'credit_card', 'blik', 'voucher', 'bank_transfer']

# Kategorie produktów i odpowiadające im listy produktów
products_by_category = {
    'Laptopy':    ['Laptop gamingowy', 'Ultrabook', 'Laptop biznesowy', 'Laptop 2w1'],
    'Smartfony':  ['Smartfon premium', 'Smartfon budzetowy', 'Smartfon ze sredniej polki', 'Smartfon dla graczy'],
    'Audio':      ['Sluchawki bezprzewodowe', 'Glosnik Bluetooth', 'Soundbar', 'Kino domowe'],
    'Telewizory': ['Telewizor OLED', 'Telewizor QLED', 'Telewizor LED', 'Telewizor 4K UHD'],
    'Akcesoria':  ['Ladowarka', 'Powerbank', 'Etui na telefon', 'Kabel USB-C', 'Hub USB']
}

# Zakresy cenowe netto dla każdej kategorii
price_ranges = {
    'Laptopy':    (2000, 8000),
    'Smartfony':  (1000, 6000),
    'Audio':      (100, 3000),
    'Telewizory': (1500, 10000),
    'Akcesoria':  (30, 500)
}

# Mapowanie marek do kategorii
brands_by_category = {
    'Laptopy':    ['Apple', 'Dell', 'HP', 'Lenovo', 'Asus'],
    'Smartfony':  ['Apple', 'Samsung', 'Xiaomi', 'Sony'],
    'Audio':      ['Sony', 'JBL', 'Bose', 'Anker'],
    'Telewizory': ['Samsung', 'LG', 'Sony'],
    'Akcesoria':  ['Anker', 'Belkin', 'Samsung', 'Apple']
}

# Możliwe ilości sztuk w zamówieniu
quantities = list(range(1, 5))

# Przygotowanie listy par (produkt, kategoria) do szybkiego losowania
product_category_pairs = [
    (prod, cat)
    for cat, prods in products_by_category.items()
    for prod in prods
]

# —————————————————————————————————————————————————————————————————————
# Pool klientów do ponownych zakupów
# —————————————————————————————————————————————————————————————————————
customer_pool = []                     # lista istniejących customer_id
repeat_customer_prob = 0.4             # 40% szans na powtórne użycie istniejącego customer_id

def generate_order(order_id: int) -> dict:
    """
    Zwraca pojedyncze zamówienie z unikalnym order_id.
    Czasami używa istniejącego customer_id, aby symulować powtórne zakupy.
    """
    # Wybór regionu i losowe miasto z tego regionu
    region = random.choice(list(region_to_cities.keys()))
    city   = random.choice(region_to_cities[region])

    # Wybór kanału sprzedaży
    channel = random.choice(sales_channels)
    if channel == 'online':
        # Jeśli online - wybieramy device_type
        device_type = random.choice(online_devices)
        salesperson = None
    else:
        # Jeśli in_store - przypisujemy sprzedawcę
        device_type = 'store'
        salesperson = random.choice(store_salespersons)

    # Wybór customer_id: nowy lub istniejący
    if customer_pool and random.random() < repeat_customer_prob:
        customer_id = random.choice(customer_pool)
    else:
        customer_id = str(uuid.uuid4())
        customer_pool.append(customer_id)

    # Wybór produktu i kategorii
    product, category = random.choice(product_category_pairs)
    # Losowanie ceny netto i ilości
    min_p, max_p = price_ranges[category]
    netto         = round(random.uniform(min_p, max_p), 2)
    qty           = random.choice(quantities)
    # Obliczenie wartości brutto (z VAT 23%)
    brutto        = round(netto * qty * 1.23, 2)
    # Wybór marki pasującej do kategorii
    brand         = random.choice(brands_by_category[category])

    # Złożenie słownika zamówienia
    order = {
        'id':              order_id,
        'timestamp':       datetime.now().isoformat(),
        'store_id':        city,
        'region':          region,
        'sales_channel':   channel,
        'device_type':     device_type,
        'customer_id':     customer_id,
        'payment_method':  random.choice(payment_methods),
        'nazwa_produktu':  product,
        'marka':           brand,
        'kategoria_produktu': category,
        'ilosc':           qty,
        'cena_netto':      netto,
        'wartosc_brutto':  brutto
    }

    # Dodajemy klucz 'sprzedawca' tylko gdy zamówienie jest in_store
    if salesperson:
        order['sprzedawca'] = salesperson

    return order

if __name__ == '__main__':
    order_id = 1
    # Główny pętla generowania zamówień z pauzą między kolejnymi wywołaniami
    while True:
        print(generate_order(order_id))
        order_id += 1
        time.sleep(random.uniform(1, 3))

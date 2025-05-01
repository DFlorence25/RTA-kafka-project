import random
import uuid
from datetime import datetime

# —————————————————————————————————————————————————————————————————————
# Konfiguracja danych syntetycznych
# —————————————————————————————————————————————————————————————————————
stores = ['Warsaw-1', 'Cracow-2', 'Gdansk-3', 'Wroclaw-4']
regions = ['East', 'West', 'North', 'South']
payment_methods = ['cash', 'credit_card', 'blik', 'voucher', 'bank_transfer']

# Kategorie i produkty
products_by_category = {
    'Laptopy': ['Laptop gamingowy', 'Ultrabook', 'Laptop biznesowy', 'Laptop 2w1'],
    'Smartfony': ['Smartfon premium', 'Smartfon budżetowy', 'Smartfon ze średniej półki', 'Smartfon dla graczy'],
    'Audio': ['Słuchawki bezprzewodowe', 'Głośnik Bluetooth', 'Soundbar', 'Kino domowe'],
    'Telewizory': ['Telewizor OLED', 'Telewizor QLED', 'Telewizor LED', 'Telewizor 4K UHD'],
    'Akcesoria': ['Ładowarka', 'Powerbank', 'Etui na telefon', 'Kabel USB-C', 'Hub USB']
}

# Zakresy cenowe dla kategorii
price_ranges = {
    'Laptopy': (2000, 8000),
    'Smartfony': (1000, 6000),
    'Audio': (100, 3000),
    'Telewizory': (1500, 10000),
    'Akcesoria': (30, 500)
}

# Mapowanie marek do kategorii
brands_by_category = {
    'Laptopy': ['Apple', 'Dell', 'HP', 'Lenovo', 'Asus'],
    'Smartfony': ['Apple', 'Samsung', 'Xiaomi', 'Sony'],
    'Audio': ['Sony', 'JBL', 'Bose', 'Anker'],
    'Telewizory': ['Samsung', 'LG', 'Sony'],
    'Akcesoria': ['Anker', 'Belkin', 'Samsung', 'Apple']
}

# Możliwe ilości w zamówieniu
quantities = list(range(1, 5))

# Przygotowanie listy (produkt, kategoria)
product_category_pairs = [
    (prod, cat)
    for cat, prods in products_by_category.items()
    for prod in prods
]

def generate_order(order_id: int) -> dict:
    """Zwraca pojedyncze zamówienie z unikalnym order_id i poprawną marką"""
    product, category = random.choice(product_category_pairs)
    min_p, max_p = price_ranges[category]
    netto = round(random.uniform(min_p, max_p), 2)
    qty = random.choice(quantities)
    brutto = round(netto * qty * 1.23, 2)  # przykład obliczenia z VAT

    # Wybór marki tylko z dozwolonego zestawu dla danej kategorii
    brand = random.choice(brands_by_category.get(category, []))

    return {
        'id': order_id,
        'timestamp': datetime.now().isoformat(),
        'store_id': random.choice(stores),
        'region': random.choice(regions),
        'customer_id': str(uuid.uuid4()),
        'payment_method': random.choice(payment_methods),
        'nazwa_produktu': product,
        'marka': brand,
        'kategoria_produktu': category,
        'ilosc': qty,
        'cena_netto': netto,
        'wartosc_brutto': brutto
    }

if __name__ == '__main__':
    order_id = 1
    while True:
        order = generate_order(order_id)
        print(order)
        order_id += 1

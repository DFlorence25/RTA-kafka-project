# 📊 Real-Time Data Pipeline - Elektronika Zamówienia

## 🎯 Problem biznesowy

W dobie cyfryzacji i rosnących oczekiwań klientów firmy handlowe muszą analizować dane sprzedażowe w czasie rzeczywistym. Dzięki temu mogą:

* Reagować szybciej na zmiany trendów zakupowych 🕒
* Optymalizować stany magazynowe 📦
* Personalizować oferty i kampanie marketingowe 🎁

**Naszym celem** było zbudowanie w pełni działającego potoku danych (data pipeline), który generuje zamówienia, przesyła je przez Apache Kafka, analizuje i wizualizuje na dashboardzie.

---

## 🛠️ Co zrobiliśmy?

1. **Generator danych** (`data_generator.py`):

   * Tworzy syntetyczne zamówienia z podziałem na regiony, miasta, kanały sprzedaży i metody płatności.
   * Wprowadza losowe opóźnienia, by symulować realne obciążenie.

2. **Producent (Producer)** (`producer.py`):

   * Subskrybuje się do generatora i wysyła każdą transakcję do topiku Kafka `zamowienia_elektronika`.
   * Ustawia klucz partycji na `store_id`, by rozłożyć obciążenie równomiernie.

3. **Konsument (Consumer)** (`consumer.py`):

   * Odbiera wiadomości z Kafki.
   * Zapisuje je do dziennych plików CSV.
   * Wysyła wsady (batch) do Google Sheets, które stanowią źródło dla dashboardu Looker Studio.

4. **Dashboard**

   * Podłączony do Google Sheets za pomocą Looker Studio.
   * Pokazuje wykresy: wolumen zamówień w czasie, wartość brutto, podział na kategorie i regiony.

---

## 🚀 Jak uruchomić projekt?

1. **Sklonuj repozytorium**:

   ```bash
   git clone https://github.com/DFlorence25/RTA-kafka-project
   cd RTA-kafka-project
   ```

2. **Dodaj plik poświadczeń Google** (`creds.json`) do katalogu głównego projektu.

3. **Uruchom z Docker Compose**:

   ```bash
   docker-compose up --build
   ```

   To uruchomi:

   * Zookeeper i Kafka
   * Generator danych
   * Producer
   * Consumer (zapis CSV + Sheets)

4. **Otwórz dashboard**

   * Wejdź na Looker Studio i wybierz arkusz `source_looker` jako źródło danych.

---

## 📦 Struktura projektu

```text
real-time-pipeline/
├── data_generator.py   # Skrypt generujący zamówienia
├── producer.py         # Wysyłka zamówień do Kafki
├── consumer.py         # Odbiór, CSV + Google Sheets
├── requirements.txt    # Zależności Python
├── docker-compose.yml  # Orkiestracja kontenerów
├── Dockerfile          # Budowa obrazu Docker
└── creds.json (✏️)     # Poświadczenia Google
```

---

## 📋 Wymagania

* Docker & Docker Compose
* Konto Google z dostępem do Google Sheets i wygenerowanym kluczem serwisowym
* Python 3.9+

---

## 💡 Możliwe rozszerzenia

* Migracja danych z Google Sheets do BigQuery dla większych wolumenów 🌐
* Wykorzystanie Avro/Protobuf do wersjonowania schematu wiadomości 📐
* Rozszerzenie generatora o sezonowe i weekendowe wzorce sprzedaży 📈
* Monitorowanie metryk (Prometheus + Grafana) i alerty w przypadku opóźnień 🚨

---

<p align="center">Made with ❤️ by Zespół Analiza Danych w Czasie Rzeczywistym</p>

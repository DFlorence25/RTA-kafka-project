Opis
Projekt do generowania i przetwarzania zamówień za pomocą Apache Kafka.

Jak uruchomić:

Zainstaluj wymagane biblioteki:
pip install -r requirements.txt
Uruchom Kafkę przez Dockera:
docker-compose up -d

Stwórz topic w Kafka:
docker exec -it kafka_project-kafka-1 bash
kafka-topics --create --topic zamowienia_elektronika --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

Uruchom generator zamówień:
python dane.py
# Dockerfile

# Bazowy obraz Pythona
FROM python:3.9-slim

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy i instalujemy zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy cały kod projektu
COPY . .

# Dzięki temu logi będą wyświetlane od razu w konsoli (bez buforowania)
ENV PYTHONUNBUFFERED=1

# Domyślnie uruchamiamy generator danych,
# ale w docker-compose.yml można to nadpisać, uruchamiając producer.py lub consumer.py
ENTRYPOINT ["python"]
CMD ["data_generator.py"]
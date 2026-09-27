# Zvanična Python slika
FROM python:3.10-slim

# Radni direktorijum unutar kontejnera
WORKDIR /app

# Kopiramo fajl sa zavisnostima
COPY requirements.txt .

# Instaliramo biblioteke
RUN pip install --no-cache-dir -r requirements.txt

# Kopiramo ostatak koda
COPY . .

# FastAPI radi na portu 8000
EXPOSE 8000

# Komanda za pokretanje uvicorn servera
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
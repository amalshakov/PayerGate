FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/accounting_for_pets

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "accounting_for_pets.wsgi:application"]
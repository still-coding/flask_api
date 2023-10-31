FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY main.py config.py requirements.txt settings.env ./
COPY templates/ ./templates/
COPY storage_adapters/ ./storage_adapters/


RUN pip install --no-cache-dir --upgrade -r requirements.txt


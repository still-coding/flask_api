FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY main.py config.py requirements.txt ./
COPY templates/ ./templates/
COPY stoprage_adapters/ ./stoprage_adapters/


RUN pip install --no-cache-dir --upgrade -r requirements.txt


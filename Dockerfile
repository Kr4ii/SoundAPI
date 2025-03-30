FROM python:3.9-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y ffmpeg libsndfile1 && \
    apt-get clean

COPY requirements.txt .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

# Создание рабочих директорий
RUN mkdir -p /data/temp /data/output /app/logs

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

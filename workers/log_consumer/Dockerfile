# Worker Dockerfile для log_consumer
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей (если нужны)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода worker
COPY . .

# Создание директории для логов
RUN mkdir -p /app/logs

# Переменные окружения по умолчанию (можно переопределить через docker-compose)
ENV PYTHONUNBUFFERED=1
ENV RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
ENV RABBITMQ_LOG_QUEUE=log_queue

# Запуск worker
CMD ["python", "log_consumer.py"]


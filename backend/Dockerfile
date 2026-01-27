# Backend Dockerfile для production
FROM python:3.12-slim as builder

# Установка системных зависимостей для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim

# Установка только runtime зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копирование зависимостей из builder stage
COPY --from=builder /root/.local /root/.local

# Копирование кода приложения
COPY . .

# Убедимся, что скрипты используют установленные пакеты
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Создание директории для логов
RUN mkdir -p /app/fallback_logs

# Запуск миграций и приложения
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2"]


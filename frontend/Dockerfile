# Frontend Dockerfile для production
# Для разработки запускайте локально: npm run dev

# ============================================
# Stage 1: Builder - сборка приложения
# ============================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Установка зависимостей с кэшированием
RUN --mount=type=cache,target=/root/.npm npm ci --only=production=false

# Копирование исходного кода
COPY . .

# Переменные VITE_* должны быть установлены при сборке
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL

# Сборка приложения для production
# Читаем VITE_GOOGLE_CLIENT_ID из .env если есть
RUN if [ -f .env ]; then \
      set -a && \
      . .env && \
      set +a && \
      echo "VITE_GOOGLE_CLIENT_ID=${VITE_GOOGLE_CLIENT_ID:-not-set}" && \
      npm run build; \
    else \
      echo "Warning: .env file not found, building without it" && \
      npm run build; \
    fi

# ============================================
# Stage 2: Production - только сборка статики
# Статика будет раздаваться через отдельный nginx сервис
# ============================================
FROM node:20-alpine AS production

WORKDIR /app

# Копируем собранную статику из builder
COPY --from=builder /app/dist /app/dist

# Просто держим контейнер запущенным, статика доступна в /app/dist
# В docker-compose volume монтируется для доступа nginx
CMD ["sh", "-c", "echo 'Frontend build completed. Static files in /app/dist' && tail -f /dev/null"]

# ============================================
# Stage 3: Development - Vite dev-сервер
# ============================================
FROM node:20-alpine AS development

WORKDIR /app

# Copy package-related files
COPY package.json package-lock.json* ./

# Установка всех зависимостей (включая dev)
RUN --mount=type=cache,target=/root/.npm npm install

# Копирование исходного кода
COPY . .

# Переменные окружения для dev
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL

# Change ownership of the application directory to the node user
RUN chown -R node:node /app

# Switch to the node user
USER node

# Expose the port used by the Vite development server
EXPOSE 5173

# Запуск dev-сервера с доступом извне контейнера
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

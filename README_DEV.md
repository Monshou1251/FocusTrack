
# README_DEV

---
## 24 мая 2025 Аутентификация (Google)

### Что сделано
- Подключил на фронтенде кнопку Google Login с использованием библиотеки - google-oauth-gsi.
- Реализовал успешный вход через Google, получил от Google authorization code.
- Разобрался с особенностями Google Identity Services и пониманием flow OAuth2 для - фронтенда.
- Устранил основные ошибки CORS и проблемы с popup, связанные с политиками браузера.

---

## 23 мая 2025 Аутентификация (Google + обычная)

- Реализована форма OAuth2EmailRequestForm для логина по email (через alias username)
- Подключена и протестирована авторизация через обычный email + пароль
- Промусолил использование super().__init__() и @property в форме
- Настроен formData на фронте (URLSearchParams) для корректного запроса
- Добавлены миграции и структура БД для поддержки OAuth-провайдеров:
- Таблицы User и OAuthAccount
- Подготовлен конфиг Settings для хранения CLIENT_ID, CLIENT_SECRET
- Начата реализация регистрации через Google:
- Кнопка уже есть на фронте
- Следующим шагом — эндпоинт для приёма Google токена и создание/поиск пользователя

---
## 22 мая 2025

### Что сделано
- Перешёл на использование OAuth2PasswordBearer с email в роли username.
- Переписал эндпоинт /login с использованием OAuth2PasswordRequestForm для совместимости с OAuth2 схемой.
- Реализовал функцию get_current_user с проверкой JWT-токена и загрузкой пользователя из БД (с async SQLAlchemy).
- Объяснил и применил Pydantic-модель UserAuthForm с методом as_form для удобного приема данных из формы.
- Настроил Swagger UI (кнопка Authorize работает с OAuth2PasswordBearer).
- Ознакомился с best practices для работы с пользователями при комбинировании обычной и OAuth авторизации.
- Доделал unit тесты для слоя Auth

### Что планируется сделать дальше
- Аутентификация через google.
- Организация таблиц в БД.
- Проверить что старые эндпоинты работают с учетом регистрации через другие провайдеры.
---

## 21 мая 2025
**Юнит-тесты и мокирование**

### Что сделано
- Разобрался с Mock, AsyncMock, MagicMock и их назначением в тестах.
- Написал и адаптировал тест для register_user с полной цепочкой db.execute → .scalars() → .first().
- Изучил, как работает TestClient() и в каких случаях он нужен.
- Написал тест для authenticate_user с мокированием зависимостей db, PasswordHasher, TokenService.
- Разобрался с assert_called() и assert_awaited() — методами проверки вызова моков.
- Понял, как связаны реальные зависимости и внедрение их через интерфейсы (Dependency Inversion Principle).
- Начал применять принципы чистой архитектуры в тестировании.

### Что планируется сделать дальше
- Закончить тесты на authenticate_user, включая негативные кейсы.
- Написать юнит-тесты для TokenService и PasswordHasher.
- Перейти к написанию API/E2E тестов с использованием TestClient.
- Продолжить реализацию OAuth-авторизации (Google, GitHub).

---

## 20 мая 2025  
**Authentication module**

### Что сделано
- Реализованы эндпоинты регистрации и логина пользователей через email + пароль.  
- Внедрена система хеширования паролей через интерфейс `PasswordHasher` и реализацию `BcryptHasher`.  
- Создан интерфейс `TokenService` с реализацией `JWTTokenService` для работы с JWT-токенами.  
- Использован Dependency Injection через FastAPI `Depends` для подстановки нужных реализаций (фабрики `get_password_hasher()`, `get_token_service()`).  
- Вся бизнес-логика вынесена в слой `services/user_service.py` для чистоты архитектуры.  
- В эндпоинтах (`auth.py`) происходит только валидация запросов и вызов сервисов.  
- Использован Pydantic для валидации входных данных (`UserAuthForm`).  
- Добавлена проверка наличия пользователя при регистрации и корректной аутентификации при логине.  
- Текущая реализация работает с PostgreSQL через AsyncSession SQLAlchemy.

### Что планируется сделать дальше
- Добавить регистрацию и аутентификацию через Google OAuth.  
- Расширить поддержку OAuth-провайдеров (GitHub и другие).  
- Реализовать обработку ошибок и исключений на более детальном уровне.  
- Написать unit-тесты на сервисы и эндпоинты.

---



<!-- prettier-ignore-start -->

# 📁 Project Structure

```plaintext

app/
│
├── api/
│   └── v1/
│       ├── dependencies.py
│       └── endpoints/
│
├── core/
│   ├── config.py
│   ├── dependencies.py
│   ├── enums.py
│   ├── interfaces.py
│   ├── responses.py
│   ├── security.py
│   └── logging/
│       └── events.py
│
├── db/
│   ├── base.py
│   ├── session.py
│   ├── models/
│   │   ├── focus.py
│   │   └── user.py
│   └── repositories/
│       ├── base.py
│       ├── focus_repo.py
│       └── user_repo.py
│
├── domain/
│   ├── entities/
│   │   ├── base.py
│   │   ├── oauth_user.py
│   │   └── user.py
│   ├── enums/
│   │   └── user_role.py
│   ├── exceptions/
│   │   ├── auth_exceptions.py
│   │   └── base.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── email/
│   │   └── logging_service.py
│   └── value_objects/
│       ├── base.py
│       ├── oauth.py
│       └── user.py
│
├── infrastructure/
│   ├── auth_providers/
│   │   ├── google_provider.py
│   │   └── sqlalchemy_user_provider.py
│   ├── messaging/
│   │   └── rabbitmq/
│   └── sqla_persistence/
│       ├── alembic/
│       ├── mappings/
│       │   ├── oauth_mapping.py
│       │   └── user_mapping.py
│       └── orm_registry.py
│
├── main.py
│
├── schemas/
│   ├── auth.py
│   └── user.py
│
└── tests/
    ├── conftest.py
    ├── api/
    │   └── test_auth_endpoints.py
    └── unit/
        ├── test_auth.py
        └── test_security.py
```

# 📁 Project Structure Overview

## 🔹 app/

Главная директория приложения, разделена по слоям в духе Clean Architecture.

### 📦 api/

- **v1/endpoints/** — роутеры для FastAPI. Разделены по сущностям (auth, user и т.д.).
- **dependencies.py** — зависимости FastAPI (например, Depends для DI).

### 📦 core/

- **config.py** — конфигурация (настройки проекта через pydantic `BaseSettings`).
- **interfaces.py** — контракты/абстракции (например, интерфейс токен-сервиса, репозиториев и т.п.).
- **security.py** — реализация авторизации, генерация JWT и т.п.
- **logging/** — кастомная система логгирования и публикации событий.

### 📦 db/

- **models/** — ORM модели SQLAlchemy.
- **repositories/** — слои доступа к данным, работающие с ORM.
- **session.py** — настройка подключения к БД через SQLAlchemy.
- **base.py** — базовые вещи для декларативного маппинга.

### 📦 domain/

- **entities/** — бизнес-сущности (Entities), не зависящие от фреймворков.
- **value_objects/** — value object'ы, например `Email`, `UserId`, `AvatarUrl` и т.п.
- **services/** — бизнес-логика (например, регистрация, логин, логгирование действий).
- **enums/** — перечисления, например, роли пользователей.
- **exceptions/** — доменные исключения.

### 📦 infrastructure/

- **auth_providers/** — реализация провайдеров (Google, Email, и т.п.).
- **sqla_persistence/** — маппинги между ORM <-> Entity, настройки SQLAlchemy.
- **messaging/rabbitmq/** — интеграция с брокером сообщений.

### 📦 schemas/

- Pydantic-схемы (DTO), используются для валидации и сериализации данных в API.

### 📦 tests/

- Модульные и API тесты.

---

# ⚙️ Модели: Entity vs ORM vs Pydantic

## 🔹 ORM-модель (SQLAlchemy)

**Где:** `app/db/models/`

Используется для работы с базой данных. Пример:

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
```

✅ Хранение в БД ❌ Не используется в бизнес-логике напрямую

## 🔹 Entity (Доменная модель)

**Где:** `app/domain/entities/`

Модель предметной области. Не зависит от БД или фреймворков.

```python
@dataclass
class User:
    id_: UserId
    email: Email
```

✅ Бизнес-логика ❌ Не сериализуется напрямую

## 🔹 Pydantic-схема

**Где:** `app/schemas/`

Модель для API. Валидирует входящие/исходящие данные.

```python
class UserOut(BaseModel):
    id: int
    email: EmailStr
```

✅ FastAPI Input/Output ❌ Не хранит бизнес-логику

---

# ✅ Когда какую модель использовать

| Задача                  | Модель   |
| ----------------------- | -------- |
| Хранение в БД           | ORM      |
| Работа в бизнес-логике  | Entity   |
| Валидация/возврат в API | Pydantic |

---

# 📌 Пример потока регистрации

1. `POST /api/auth/register` (использует Pydantic EmailRegisterForm)
2. Вызывает `auth_service.register_user(form_data)` — внутри работают Entity/ValueObjects
3. Entity маппится в ORM и сохраняется в БД
4. Возвращается UserOut (Pydantic) в ответе

---

# README_DEV

## 23 июля 2025 — Отправка данных о спринтаз на бек

- Сделал сервис по отправке запросов
- Сделал логику отправки запросов, при паузе, при стопе и тд.
- Слегка подправил роуты бека (добавить версионность).
- Сделал ендпоинт-заглушку для получения данных с фронта.

- Теперь нужно сделать полноценный эндпоинт по записи данных в базу.
- Создать сущности, маппинги и прочее.

---

## 22 июля 2025 — Переработка фронта

- Доделал логику таймера. Состояние между сессиями сохраняется, при паузе
  состояние запоминается, в общем всё ок, можно приступать к работе с беком.

- Нужно сделать заглушки на фронте, имитация отправки запросов по сессиям.
- И вообще надо бы продумать когда и как будут эти запросы слаться,
  и что должно быть в запросе. Думаю напишу просто небольшой сервис,который буду вызывать где мнге нужно, а какие даты слать, нуждно будет смотреть в сущности бека, что он там переваривает.

---

## 19 июля 2025 — Переработка фронта

- Заменил heatmap на свой пакет (для этого его сначала разработал).
  Теперь он сделан на основе div и я могу как хочу его менять, а не то что раньше
  кто вообще делает такие вещи на базе svg... нелюди страшные.
- Вынес всю логику работы таймера в store, а точнее timer.ts
- И да, начал переводить всё на TS

- Сейчас не работает сохранение состояиния таймера между сессиями, то есть надо логику слегка поменять.

Перерыв был большой конечно, но часть я потратил на работу а часть на разработку пакета.

---

## 3 июля 2025 — Модели, чистая архитектура, маппинги

- Завершил проектирование моделей `Category`, `Sprint`.
- Сделал связи `relationship` между пользователем, категориями и спринтами.
- Провёл миграции через Alembic, все таблицы успешно создались.
- Начал писать `Entity` и `ValueObject` для `Category`.
- Написал маппинг `category_orm_to_entity` и обратно.
- Столкнулся с ошибками mypy и Pylance по типам `Mapped[...]`, утомителя хрень.
  Вообще mypy, Pylance очень как-то криво совместимы с SQLAlchemy моделями.

---

## 30 июня 2025 — Аутентификация, флоу, анимация

- Доделал аутентификция через гугл
- Добавил анимацию.
- Дефолтный урл аватарки не сделал, печаль, просто лениво сегодня

---

## 29 июня 2025 — Обратный таймер, переключение на режим Rest

- Логика аутентификации доделана (за искл гугл)
- Переадресация работает, роутер настроен
- Работа с куки настроена, это была некая попная боль. jwt хранится в http-only cookie
- Передача и исп данных в сторе с бека на фронт настроена.
- Добавлен простенький защищеный эндпоинт me, он выдает данные для фронта.
- Добавлен простенький эндпоинт для выхода.
- Логика выхода (удаление куки и тп) сделана как на фронте так и на беке.

### Дальше

- Нужно доделать аутентификацию с гуглом (также хранение кук и тп)
- Нужно решить с дефолтным урлом (аватаром), вроде бы сделал дефолтное значение в бд, но чет не работает.
- Сделать какую-нибудь простенькую анимацию при входе.

---

## 27 июня 2025 — Обратный таймер, переключение на режим Rest

- Основной таймер:
  - Переработан в **обратный отсчёт** (countdown) на основе `currentPace` из store
  - Показываются только **минуты и секунды**
  - Таймер обновляется через `setInterval`, основываясь на `Date.now()`
- Реализована **смена режима**:
  - После окончания фокус-фазы (`focus`) переключается в режим отдыха (`rest`)
  - Значение `remainingTime` сбрасывается на `currentRest` из store
  - Таймер **не стартует автоматически**, ожидает нажатия кнопки
- Введено новое поле `mode` (`focus` / `rest`) для контроля состояния
- Все цифры таймера работают через `computed` поля, форматируются с `padStart(2, '0')`
- Обновлён `resetTimer()` — теперь сбрасывает `remainingTime` в зависимости от текущего режима
- Подготовлена логика для будущей поддержки повторных циклов и смены расцветки / UI при переходе в `rest`

---

## 26 июня 2025 — Верстка, логика UI и состояния

- Подключён и настроен **Pinia** для глобального состояния
- Реализовано:
  - Добавление, редактирование, удаление **категорий**
  - Назначение **цветов** категориям через store
  - Сохранение выбранной категории в store (`selectedCategory`)
- Компонент `AppButton` переделан под **выпадающий список** и разделен на три компонента отдельных `CategoriesButton`, `PaceButton`, `RestButton`
  - Показывает текущую категорию с цветом
  - Автоматически скрывается при клике вне
  - Скрывает слишком длинные названия (с `...`)
- Добавлены **выпадающие списки для Pace и Rest**
  - План: сохранять значения в store и ограничивать таймер по ним
- Таймер:
  - Старт, пауза, сброс
  - Сохраняет время в `localStorage` между сессиями
- Обсуждены подходы:
  - Разделение компонентов (`Categories`, `Pace`, `Rest`)
  - Перенос логики в store

---

## 25 июня 2025 - Верстка, функционал фронта

- Работа над фронтом
- Heat map добавлен и настроен
- Категории добавлены и настроены

---

## 24 июня 2025 - Верстка, функционал фронта

- Работа над фронтом

---

## 23 июня 2025 - Верстка, функционал фронта

- Работа над фронтом

---

## 22 июня 2025 - Верстка, функционал фронта

- Работа над фронтом

---

## 21 июня 2025 - Верстка, функционал фронта

- Пропустил несколько записей.
- Главный компонент сделан, таймер работает, при перезагрузке сохраняется текущий статус.
- Создал компоненты кнопок
- Также доделан navbar
- В общем много всего сделано.

Дальше компнонет Категорий

---

## 18 июня 2025 - Верстка

- Верстка главной страницы.

---

## 16 июня 2025 - Верстка

- Верстка, назначение общих переменных css, разметка страницы, навбар в зависимости от статуса входа.

---

## 14 июня 2025 - Фигма + переделка модели

- Макет фигмы закончил, буду приступал к верстке и базовой логике роутеров.
- Добавил поле avatar_url в модель User, поправил сущность, мэппинг, создал value_object для avatar

---

## 9 июня 2025 - Фигма

- Начал работу над макетом, в очередной раз убедился что дизайн это та ещё попная боль. Пока что просто наметил функциональные блоки, шрифты, цвета.

---

## 8 июня 2025 - ебалумба

- Даже нет сил описывать что было сделано. Часов 12 ушло на создание сущностей , правильное их разделение, на содание value_objects, enums, и самое главнгое мэппингов. Мы же модные, мы же крутые, мы должнгы следовать DDD, мать его в кино водил. И пришлось раззделять интерфейсы (что собственно правильно) UserRepository, а также добавлять сущности для UserOAuthAccount, ну и мэппинги. И вот с этой ебалумбой конфликтов типа и прочего я воевал и довоевал. Не работало ничего, сейчас вё работает.
  Мне нужно остановиться уже на блоке аутентификации, а это будет бесконенчо.

### Дальше

- Пора может уже начать функционал делать не? - всё такой же план

---

## 7 июня 2025 - Сущности

- Нащел ошибку, которая нарушает принцип чистой чистоты, это интерфейс , где я импортил модель User прям из слоя db, что есть очень не гуд. Чтобы решить жто проблему я создал сущность (entity) user.py в слое domain/entities.
  Но не все так просто, для корректности пришлось value_objects, чтобы проверять поля email, user_id, uer_password_hash, username. Также я осздал папку enums , в том же слое, в ней описываю user_role, чтобы потом в коде легко обращаться так:
  username.ADMIN например. Потом я понял что собсна поля role вообще нет в модели alembic, создал миграцию, в процессе миграции добавил поле, добавил тип Enum в базе. Провёл миграцию, всё ок, доволен нраится!

### Дальше

- Пора может уже начать функционал делать не? - всё такой же план

---

## 4 июня 2025 - Форматтеры, линтеры и прочие шляпы

- Настроил все эти приблуды таким образом:
- black - форматтер
- ruff - линтинг, автофиксы, стиль, импорты
- mypy - проверка типов, особенно для pydantic
- Поработал с типами функций
- Слегка подправил окружение vscode
- Переделал oauth эндпоинт с логгированием, всё работает всё ок.
- Решил все явные проблемы с типами и аннотациями

### Дальше

- Пора может уже начать функционал делать не?

---

## 3 июня 2025 Проверка и валидация форм регистрации и логина в FastAPI

- Переписал логирование, сделал всё красиво и четко, создал более чистый независимый блок с логированием.
  Вот так выглядит примерная стуктура:
  Компоненты логирования:
  Интерфейс LogPublisher
  Находится в core/interfaces.py.
  Определяет метод publish(event: LogEvent) — абстракция для всех логеров.

События логов (LogEvent)
Находятся в core/logging/events.py.
Абстрактный класс LogEvent и конкретный UserLoginAttemptLog, который содержит email, IP, success и error.
Метод to_dict() — сериализация события.

Сервис логирования (log_auth_attempt)
Находится в domain/services/logging_service.py.
Принимает LogPublisher, создает событие и вызывает .publish().

Реализация логера (RabbitMQLogPublisher)
Находится в infrastructure/messaging/.
Реализует LogPublisher, подключается к RabbitMQ, отправляет LogEvent.to_dict().

Зависимость (get_log_publisher)
В core/dependencies.py.
Возвращает инстанс RabbitMQLogPublisher.

Эндпоинт /login
Получает log_publisher: LogPublisher = Depends(get_log_publisher)
И вызывает:
asyncio.create_task(log_auth_attempt(...))

- asyncio.create_task появилось из-за того что появилась проблема. Я специально отрубил rabbit, чтобы поглядеть как себя поведет приложение. Ну и конечно же всё слегко. тогда я добавил логику, что если кроличья морда упала, то логи пишутся в **fallback_logs**.
  Дальше я заметил что появилась задержка при отключенном рэббите. Очевидно операция была блокирующая, то есть таймаут попытки коннекта к рэббиту 5 сек. Поэтому я сделал логгирование корутиной, а в эндпоинте через asyncio запихал эту корутину в таску и всё.

### Дальше

- Нужно подумать что делать дальше, в фигме полепить примерный вайрфрейм главной страницы, или же нет...
- Ну и самое важнео это добавить логирование ещё в oauth сущности.
- В общем стремлюсб к mvp , а дальше как пойдет.
- Логирование OAuth не доделано, обработку ответов нужно переделать.

---

## 2 июня 2025 Проверка и валидация форм регистрации и логина в FastAPI

- Переписал валидацию форм с помощью Pydantic моделей, добавил методы `as_form` для корректного парсинга form-data в эндпоинтах.
- Настроил строгую валидацию email и пароля (мин длина, не пустые поля) на уровне Pydantic — теперь 422 ошибки срабатывают ещё до вызова бизнес-логики.
- Сделал кастомные исключения и хендлинг ошибок в эндпоинтах с единым форматом ответа `success`/`message`.
- Реализовал разделение моделей логина и регистрации: создал базовую модель с общими полями и унаследовал её с переопределением требований к паролю для регистрации.
- Создал слой domain, очистил services полностью от каких-либо конкретных зависимостей реализации.
- Создал интерфейсы кастомных ошибок

### Дальше

- Продолжить улучшать обработку ошибок и юнит-тестировать формы.
- Реализовать аналогичную валидацию для OAuth форм.
- Подумать над централизованным логированием ошибок и их мониторингом.

---

## 30 мая 2025 Аутентификация (responses)

- Добавлены хелперы для унификации responses, добавлены схемы для этих хелперов (responses_schemas)
- Настроил логирование через RabbitMQ, задел на будущее, планирую сохранять логи в Elasticsearch, пока что сохраняю в backend/logs/logs.jsonl

### Дальше

- Пора уже приступать к функционалу, хотя супер лень :3
- Нужно поправить сервис аутентификации, вынести логгер в хелпер, иначе сейчс половину кода занимает логгер..
- Залогировать все имеющиеся сервисы

---

## 29 мая 2025 Аутентификация (Google, OAuth)

- Доделал вход и регистрацию через oauth
- SQLAlchemyUserRepository обновил, добавил методы для работы с oauth (get_user_by_oauth, create_oauth_user, create_oauth_account)
- Добавлен интерфейс OAuthProvider
- Добавлен серивс oauth_login вкратце что там делается:

* Обменивает code на access_token через выбранного OAuthProvider
* Получает информацию о пользователе с помощью access_token
* Ищет пользователя в базе по связке provider + provider_id
* Если не найден — ищет по email, и если тоже не найден — создаёт нового пользователя
* Создаёт запись об OAuth-аккаунте, если её нет
* Генерирует JWT-токен и возвращает его клиенту

---

## 26 мая 2025 Аутентификация (Google, OAuth)

- Разнес логику аутентифицкации и регистрации. Теперь всё красиво.
- Создан интерфейс UserRepository с методами get_by_email, exists_by_email, create_user
- Создана реализация SQLAlchemyUserRepository

### Дальше

- Завязать OAuth аутентификацию на работу с базой.

---

## 25 мая 2025 Аутентификация (Google, OAuth)

- Добавил новый слой инфраструктуры, там будет реализация всего и вся, непосредственно работа с db и прочим.
- В слой добавил oauth_providers , папка для определения реализации аутентификации по oauth.
- Реализовал в том же слое google_provider.py, всё работает всё ок, получаю все нужные данные, остается только завязать на работу с базой.
- Так же добавил интерфейс для работы с oauth - OAuthProvider(Protocol)

### Что сделать

- Переписать логику authenticate_user и register_user, нужно вынести реализацию в слой infrastructure
- Так же нужно обновить логику чтобы всё работало с oauth.
- Ну и дописать логику самого google auth (регистрация и вход)

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
- Промусолил использование super().**init**() и @property в форме
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

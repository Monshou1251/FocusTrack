import pytest
from unittest.mock import AsyncMock, MagicMock, Mock
from app.services.user_service import register_user, authenticate_user
from app.schemas.user import UserCreate
from app.schemas.auth import UserAuthForm
from app.db.models.user import User
from app.core.interfaces import PasswordHasher, TokenService


# Простой хешер для теста — имитирует поведение настоящего
class DummyHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed-{password}"
    
    def verify(self, plain: str, hashed: str) -> bool:
        return plain == "correct_password" and hashed == "hashed_password"


class DummyTokenService(TokenService):
    def create_token(self, data: dict) -> str:
        return "mocked_token"


@pytest.mark.asyncio
async def test_register_user_success():
    # Создаём мок сессии
    mock_session = AsyncMock()

    # Примерно так работает цепочка:
    # db.execute(...) → result → result.scalars() → first()
    # Нам нужно смоделировать каждый шаг

    # Возвращаемое значение от .execute()
    mock_execute_result = Mock()

    # Возвращаемое значение от .scalars()
    mock_scalars = Mock()
    mock_scalars.first.return_value = None  # пользователь не найден

    # Подключаем .scalars() к результату
    mock_execute_result.scalars.return_value = mock_scalars
    # Подключаем .execute() к сессии
    mock_session.execute.return_value = mock_execute_result

    # ВАЖНО: .add() — синхронная функция, нужно мокать через обычный Mock
    mock_session.add = Mock()

    # .commit() и .refresh() — асинхронные, мокаем через AsyncMock
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    # Создаём данные пользователя
    user_data = UserCreate(email="test@example.com", password="secret")
    hasher = DummyHasher()

    # Вызываем функцию, которую тестируем
    result = await register_user(user_data, mock_session, hasher)

    # Проверяем результат — функция должна вернуть словарь с сообщением
    assert result == {"msg": "User created successfully."}

    # Проверяем, что пользователь был добавлен в сессию
    mock_session.add.assert_called()

    # Проверяем, что транзакция была сохранена
    mock_session.commit.assert_awaited()

    # Проверяем, что объект пользователя был обновлён из БД
    mock_session.refresh.assert_awaited()


@pytest.mark.asyncio
async def test_authenticate_user_success():
    # 📦 Подготовка (Arrange)

    # 1. Мокаем асинхронную сессию
    mock_session = AsyncMock()

    # 2. Мокаем результат .execute()
    mock_execute_result = Mock()

    # 3. Мокаем возвращаемого пользователя из .scalar()
    mock_user = Mock(spec=User)
    mock_user.email = "test@example.com"
    mock_user.hashed_password = "hashed_password"

    mock_execute_result.scalar.return_value = mock_user
    mock_session.execute.return_value = mock_execute_result

    # 4. Создаём форму с правильным паролем
    form_data = UserAuthForm(email="test@example.com", password="correct_password")

    # 5. Подключаем поддельные зависимости
    hasher = DummyHasher()
    token_service = DummyTokenService()

    # 🧪 Действие (Act)
    result = await authenticate_user(form_data, mock_session, hasher, token_service)

    # ✅ Проверка (Assert)
    assert result == {
        "access_token": "mocked_token",
        "token_type": "bearer"
    }
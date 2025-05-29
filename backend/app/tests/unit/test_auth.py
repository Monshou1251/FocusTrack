import pytest
from unittest.mock import AsyncMock, Mock
from app.services.auth_service import register_user, authenticate_user
from app.schemas.user import UserCreate
from app.schemas.auth import UserAuthForm
from app.db.models.user import User
from app.core.interfaces import PasswordHasher, TokenService
from app.infrastructure.auth_providers.sqlalchemy_user_provider import SQLAlchemyUserRepository
from fastapi import HTTPException, status


class DummyHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed-{password}"
    
    def verify(self, plain: str, hashed: str) -> bool:
        return hashed == self.hash(plain)



class DummyTokenService(TokenService):
    def create_token(self, data: dict) -> str:
        return "mocked_token"


@pytest.fixture
def mock_db_user_found():
    mock_session = AsyncMock()
    mock_execute_result = Mock()
    mock_scalars = Mock()
    mock_user = Mock(spec=User)
    mock_user.email = "test@example.com"
    mock_user.hashed_password = "hashed_password"
    
    mock_scalars.first.return_value = mock_user
    mock_execute_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_execute_result
    
    return mock_session, mock_user


@pytest.mark.asyncio
async def test_register_user_success():
    mock_session = AsyncMock()

    mock_execute_result = Mock()
    mock_scalars = Mock()
    mock_scalars.first.return_value = None 
    mock_execute_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_execute_result

    mock_session.add = Mock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    user_data = UserCreate(email="test@example.com", password="secret")
    hasher = DummyHasher()

    repo = SQLAlchemyUserRepository(mock_session)
    result = await register_user(user_data, repo, hasher)

    assert result == {"msg": "User created successfully."}
    mock_session.add.assert_called()
    mock_session.commit.assert_awaited()
    mock_session.refresh.assert_awaited()


@pytest.mark.asyncio
async def test_register_user_existing_email(mock_db_user_found):
    mock_session, _ = mock_db_user_found
    form_data = UserCreate(email="test@example.com", password="123")
    hasher = DummyHasher()

    with pytest.raises(HTTPException) as exc_info:
        await register_user(form_data, mock_session, hasher)

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_authenticate_user_success():
    # Arrange
    form_data = UserAuthForm(email='test@example.com', password='correct_password')
    
    user_repo = AsyncMock()
    hasher = DummyHasher()
    token_service = DummyTokenService()

    mock_user = Mock()
    mock_user.email = form_data.email
    mock_user.hashed_password = hasher.hash("correct_password")
    mock_user.auth_provider = "email"

    # Мокаем метод get_user_by_email
    user_repo.get_user_by_email.return_value = mock_user

    # Act
    result = await authenticate_user(form_data, user_repo, hasher, token_service)

    # Assert
    assert result == {
        "access_token": "mocked_token",
        "token_type": "bearer"
    }

    user_repo.get_user_by_email.assert_awaited_once_with(form_data.email)


@pytest.mark.asyncio
async def test_authenticate_user_fail(mock_db_user_found):
    mock_session, _ = mock_db_user_found
    
    form_data = UserAuthForm(
        email="failed_test_user@example.com",
        password="wrong_password"
    )
    
    hasher = DummyHasher()
    token_service = DummyTokenService()
    
    with pytest.raises(HTTPException) as exc_info:
        await authenticate_user(form_data, mock_session, hasher, token_service)
        
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Incorrect email or password"


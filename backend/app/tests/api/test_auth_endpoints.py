# # tests/test_auth.py

# import pytest
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import FastAPI
# from app.main import app  # твое приложение FastAPI
# from app.db.models.user import User
# from app.core.security import get_password_hasher  # или свой DummyHasher
# from app.schemas.user import UserAuthForm

# # допустим ты используешь SQLite в памяти или FastAPI dependency overrides

# @pytest.mark.asyncio
# async def test_login_success(async_session: AsyncSession):
#     # Предварительно создаём пользователя в базе
#     from app.core.security import password_hasher  # или используй фикстуру

#     user = User(
#         email="test@example.com",
#         hashed_password=password_hasher.hash("correct_password")
#     )
#     async_session.add(user)
#     await async_session.commit()

#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post(
#             "/login",
#             json={"email": "test@example.com", "password": "correct_password"}
#         )

#     assert response.status_code == 200
#     assert response.json()["access_token"]  # или полное сравнение, если знаешь значение

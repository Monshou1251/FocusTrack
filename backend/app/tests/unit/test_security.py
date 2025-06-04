import time
from datetime import timedelta

import pytest

from app.core.security import BcryptHasher, JWTTokenService


@pytest.fixture
def hasher():
    return BcryptHasher()


@pytest.fixture
def token_service():
    return JWTTokenService()


# tests for BcryptHasher
def test_hash_and_verify(hasher):
    password = "mysecretpassword"
    hashed_password = hasher.hash(password)

    assert hashed_password != password
    assert hasher.verify(password, hashed_password)
    assert not hasher.verify("wrongpass", hashed_password)


# tests for JWTTokenService
def test_create_and_verify_token(token_service):
    data = {"sub": "test@test.com"}
    token = token_service.create_token(data)
    decoded = token_service.verify_token(token)

    assert decoded is not None
    assert decoded["sub"] == data["sub"]
    assert "exp" in decoded


def test_token_expiration(token_service):
    data = {"sub": "test@test.com"}
    token = token_service.create_token(data, expires_delta=timedelta(seconds=1))
    time.sleep(2)
    decoded = token_service.verify_token(token)
    assert decoded is None


def test_invalid_token(token_service):
    invalid_token = "this.is.not.a.valid.token"
    decoded = token_service.verify_token(invalid_token)
    assert decoded is None

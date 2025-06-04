from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# pyright: reportGeneralTypeIssues=false


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String, nullable=True)
    auth_provider = Column(String, default="email", nullable=False)

    oauth_accounts = relationship(
        "OAuthAccount", back_populates="user", cascade="all, delete-orphan"
    )


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)
    provider_id = Column(String, unique=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="oauth_accounts")

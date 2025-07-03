from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.category import Category
    from app.db.models.user import User


class Sprint(Base):
    __tablename__ = "sprints"
    __table_args__ = (
        CheckConstraint(
            "target_minutes IN (15, 30, 45, 60, 75, 90)", name="valid_target_minutes"
        ),
        CheckConstraint("actual_minutes >= 0", name="non_negative_actual_minutes"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_minutes: Mapped[int] = mapped_column(nullable=False)
    actual_minutes: Mapped[int] = mapped_column(nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="sprints")
    category: Mapped["Category"] = relationship(back_populates="sprints")

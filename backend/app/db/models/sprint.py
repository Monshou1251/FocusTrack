from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy import DateTime as SQLAlchemyDateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.category import Category
    from app.db.models.user import User


class Sprint(Base):
    __tablename__ = "sprints"
    __table_args__ = (
        CheckConstraint("duration >= 0", name="non_negative_actual_minutes"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    duration: Mapped[int] = mapped_column(nullable=False)

    started_at: Mapped[datetime] = mapped_column(
        SQLAlchemyDateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="sprints")
    category: Mapped["Category"] = relationship(back_populates="sprints")

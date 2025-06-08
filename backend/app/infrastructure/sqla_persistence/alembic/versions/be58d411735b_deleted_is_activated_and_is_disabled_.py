"""Deleted is_activated and is_disabled fields for now

Revision ID: be58d411735b
Revises: a4d7dd11c635
Create Date: 2025-03-29 21:29:57.226859

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "be58d411735b"
down_revision: str | None = "a4d7dd11c635"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

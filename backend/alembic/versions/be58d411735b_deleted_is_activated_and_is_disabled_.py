"""Deleted is_activated and is_disabled fields for now

Revision ID: be58d411735b
Revises: a4d7dd11c635
Create Date: 2025-03-29 21:29:57.226859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be58d411735b'
down_revision: Union[str, None] = 'a4d7dd11c635'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

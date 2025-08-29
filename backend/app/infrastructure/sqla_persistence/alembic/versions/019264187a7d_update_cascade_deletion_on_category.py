"""Update cascade deletion on category

Revision ID: 019264187a7d
Revises: aaf21a88baa8
Create Date: 2025-08-30 00:12:00.906086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '019264187a7d'
down_revision: Union[str, None] = 'aaf21a88baa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

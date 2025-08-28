"""merge heads

Revision ID: e79229f2dbc6
Revises: add_journal_entries_table, d3c69e5ac749
Create Date: 2025-08-23 04:29:22.830254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e79229f2dbc6'
down_revision: Union[str, None] = ('add_journal_entries_table', 'd3c69e5ac749')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

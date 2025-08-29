"""Update nullable to sprint model

Revision ID: aef3327c90e4
Revises: f29a9008905f
Create Date: 2025-08-30 00:21:59.115930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aef3327c90e4'
down_revision: Union[str, None] = 'f29a9008905f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

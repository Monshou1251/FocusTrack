"""Update nullable to sprint model

Revision ID: f1e9ae59fd43
Revises: aef3327c90e4
Create Date: 2025-08-30 00:22:42.948622

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1e9ae59fd43"
down_revision: str | None = "aef3327c90e4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("sprints", "category_id", existing_type=sa.Integer(), nullable=True)


def downgrade() -> None:
    op.alter_column(
        "sprints", "category_id", existing_type=sa.Integer(), nullable=False
    )

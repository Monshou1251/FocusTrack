"""Added user model with email verification

Revision ID: ee4519a603d4
Revises: c29dcc7d7207
Create Date: 2025-03-01 02:35:54.700310

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ee4519a603d4"
down_revision: str | None = "c29dcc7d7207"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=True))
    op.add_column("users", sa.Column("is_verified", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "is_verified")
    op.drop_column("users", "is_active")
    # ### end Alembic commands ###

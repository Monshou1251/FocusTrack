"""Add role column to user

Revision ID: 907e91ecb02e
Revises: 1350b32e50bc
Create Date: 2025-06-07 19:04:38.780215

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "907e91ecb02e"
down_revision: str | None = "1350b32e50bc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

user_role_enum = sa.Enum("SUPER_ADMIN", "ADMIN", "USER", name="userrole")


def upgrade():
    user_role_enum.create(op.get_bind(), checkfirst=True)

    op.add_column("users", sa.Column("role", user_role_enum, nullable=True))

    op.execute("UPDATE users SET role = 'USER'")

    op.alter_column("users", "role", nullable=False)


def downgrade():
    op.drop_column("users", "role")

    user_role_enum.drop(op.get_bind(), checkfirst=True)

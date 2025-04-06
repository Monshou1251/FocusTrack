"""Remove is_active and is_verified from User

Revision ID: c6715e26fedf
Revises: be58d411735b
Create Date: 2025-03-29 21:31:46.953223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6715e26fedf'
down_revision: Union[str, None] = 'be58d411735b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('is_verified', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

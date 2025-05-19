"""adding password field to users table

Revision ID: 1a97142797b4
Revises: 7348237bfb5c
Create Date: 2025-05-11 09:55:20.834811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a97142797b4'
down_revision: Union[str, None] = '7348237bfb5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("password", sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column("users", "password")
    pass

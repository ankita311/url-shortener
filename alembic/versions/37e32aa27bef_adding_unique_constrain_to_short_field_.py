"""adding unique constrain to short field in url

Revision ID: 37e32aa27bef
Revises: 3a014e455686
Create Date: 2025-05-19 20:16:55.547109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37e32aa27bef'
down_revision: Union[str, None] = '3a014e455686'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('urls', 'short', new_column_name='short_code')
    op.create_unique_constraint('uq_short_code', 'urls', ['short_code'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_short_code', 'urls', type_='unique')
    op.alter_column('urls', 'short_code', new_column_name='short')

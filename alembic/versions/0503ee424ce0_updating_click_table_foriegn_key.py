"""updating click table foriegn key

Revision ID: 0503ee424ce0
Revises: ed53dc076d2e
Create Date: 2025-06-08 19:35:37.269988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0503ee424ce0'
down_revision: Union[str, None] = 'ed53dc076d2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('clicks_url_id_fkey', 'clicks', type_='foreignkey')
    op.create_foreign_key(None, 'clicks', 'urls', ['url_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'clicks', type_='foreignkey')
    op.create_foreign_key('clicks_url_id_fkey', 'clicks', 'urls', ['url_id'], ['id'])
    # ### end Alembic commands ###

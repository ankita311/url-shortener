"""adding token blacklist table

Revision ID: 3a014e455686
Revises: 1a97142797b4
Create Date: 2025-05-18 11:20:03.919569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a014e455686'
down_revision: Union[str, None] = '1a97142797b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('token_blacklist', 
                    sa.Column('id', sa.Integer, primary_key = True),
                    sa.Column('jti', sa.String, nullable=False),
                    sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.UniqueConstraint('jti'))


def downgrade() -> None:
    op.drop_table('token_blacklist')
    

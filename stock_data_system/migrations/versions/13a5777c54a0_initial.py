"""initial

Revision ID: 13a5777c54a0
Revises: 
Create Date: 2025-03-06 23:03:16.637650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13a5777c54a0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('stock_info',
        sa.Column('symbol', sa.String(length=10), primary_key=True),
        sa.Column('name', sa.String(length=50)),
        sa.Column('exchange', sa.String(length=10)),
        sa.Column('industry', sa.String(length=50)),
        sa.Column('list_date', sa.String(8)),
        sa.Column('status', sa.String(8), server_default='L')
    )
    op.create_table('daily_data',
        sa.Column('date', sa.Date(), primary_key=True),
        sa.Column('symbol', sa.String(length=10), primary_key=True),
        sa.Column('open', sa.Float()),
        sa.Column('high', sa.Float()),
        sa.Column('low', sa.Float()),
        sa.Column('close', sa.Float()),
        sa.Column('volume', sa.Integer())
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('daily_data')
    op.drop_table('stock_info')

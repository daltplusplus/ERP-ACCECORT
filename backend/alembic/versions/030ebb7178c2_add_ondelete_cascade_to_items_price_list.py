"""add ondelete cascade to items_price_list

Revision ID: 030ebb7178c2
Revises: 72da3dc6b392
Create Date: 2025-10-18 23:20:33.276570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '030ebb7178c2'
down_revision: Union[str, Sequence[str], None] = '72da3dc6b392'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

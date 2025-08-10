"""merge heads

Revision ID: 28618af5f61d
Revises: 012d0db42458, cc4e71966d39
Create Date: 2025-08-10 09:20:39.935084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28618af5f61d'
down_revision: Union[str, Sequence[str], None] = ('012d0db42458', 'cc4e71966d39')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

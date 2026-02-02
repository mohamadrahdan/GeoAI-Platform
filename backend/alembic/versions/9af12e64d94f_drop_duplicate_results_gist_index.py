"""drop duplicate results gist index

Revision ID: 9af12e64d94f
Revises: 9db12c372ecd
Create Date: 2026-02-02 13:00:42.490054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9af12e64d94f'
down_revision: Union[str, Sequence[str], None] = '9db12c372ecd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

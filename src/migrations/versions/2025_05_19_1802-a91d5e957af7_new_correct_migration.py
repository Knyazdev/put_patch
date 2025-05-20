"""new correct migration

Revision ID: a91d5e957af7
Revises: cc454f1608f9
Create Date: 2025-05-19 18:02:18.348253

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a91d5e957af7"
down_revision: Union[str, None] = "cc454f1608f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

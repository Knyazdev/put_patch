"""rename column in hotel table

Revision ID: 761456864118
Revises: ab641f793602
Create Date: 2025-05-19 17:53:42.233027

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "761456864118"
down_revision: Union[str, None] = "ab641f793602"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(table_name="hotels", column_name="name", new_column_name="title")


def downgrade() -> None:
    op.alter_column(table_name="hotels", column_name="title", new_column_name="name")

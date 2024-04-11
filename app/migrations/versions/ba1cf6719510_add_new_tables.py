"""Add new tables

Revision ID: ba1cf6719510
Revises: 297878f4494f
Create Date: 2024-03-22 14:16:13.489083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba1cf6719510'
down_revision: Union[str, None] = '297878f4494f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

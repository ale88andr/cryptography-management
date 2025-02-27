"""Update key_document table

Revision ID: 28320fabc47b
Revises: 984e5220a25d
Create Date: 2025-02-27 08:49:20.135943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28320fabc47b'
down_revision: Union[str, None] = '984e5220a25d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE actrecordtypes ADD VALUE 'KD_REPLACE'")


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

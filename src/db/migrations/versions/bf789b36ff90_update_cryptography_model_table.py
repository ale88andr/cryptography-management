"""Update cryptography_model table

Revision ID: bf789b36ff90
Revises: ea6bf6d5f141
Create Date: 2025-03-06 08:00:20.305041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bf789b36ff90'
down_revision: Union[str, None] = 'ea6bf6d5f141'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cryptography_model', 'product_type_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('cryptography_model', 'type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cryptography_model', sa.Column('type', postgresql.ENUM('PROGRAM', 'HARDWARE', 'HARDSOFT', name='modeltypes'), autoincrement=False, nullable=False))
    op.alter_column('cryptography_model', 'product_type_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###

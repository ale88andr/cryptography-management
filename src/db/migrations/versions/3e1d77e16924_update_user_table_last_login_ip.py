"""Update user table last_login_ip

Revision ID: 3e1d77e16924
Revises: c321fe95d341
Create Date: 2024-11-29 07:49:48.033850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e1d77e16924'
down_revision: Union[str, None] = 'c321fe95d341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_login_ip', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_login_ip')
    # ### end Alembic commands ###

"""Update location table

Revision ID: 674eba01928b
Revises: 38a5d8daa376
Create Date: 2024-11-05 13:16:00.997084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '674eba01928b'
down_revision: Union[str, None] = '38a5d8daa376'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('employee_location_name_key', 'employee_location', type_='unique')
    op.create_unique_constraint('name_building', 'employee_location', ['name', 'building_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('name_building', 'employee_location', type_='unique')
    op.create_unique_constraint('employee_location_name_key', 'employee_location', ['name'])
    # ### end Alembic commands ###

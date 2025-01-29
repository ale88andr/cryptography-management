"""Update organisation table: add responsible users

Revision ID: 8af009d58bc1
Revises: 80901f23a236
Create Date: 2025-01-27 08:37:45.488503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8af009d58bc1'
down_revision: Union[str, None] = '80901f23a236'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee_organisation', sa.Column('responsible_employee_id', sa.Integer(), nullable=True))
    op.add_column('employee_organisation', sa.Column('spare_responsible_employee_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'employee_organisation', 'employee', ['responsible_employee_id'], ['id'])
    op.create_foreign_key(None, 'employee_organisation', 'employee', ['spare_responsible_employee_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employee_organisation', type_='foreignkey')
    op.drop_constraint(None, 'employee_organisation', type_='foreignkey')
    op.drop_column('employee_organisation', 'spare_responsible_employee_id')
    op.drop_column('employee_organisation', 'responsible_employee_id')
    # ### end Alembic commands ###

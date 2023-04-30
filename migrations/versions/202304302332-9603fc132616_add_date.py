"""add date

Revision ID: 9603fc132616
Revises: a5e1d4e1dbeb
Create Date: 2023-04-30 23:32:12.912515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9603fc132616'
down_revision = 'a5e1d4e1dbeb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('point_value', sa.Column('date', sa.DateTime(), server_default='', nullable=False))
    op.create_index(op.f('ix_point_value_date'), 'point_value', ['date'], unique=False)
    # ### end Alembic commands ###
    op.execute('update point_value set `date` = datetime()')

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_point_value_date'), table_name='point_value')
    op.drop_column('point_value', 'date')
    # ### end Alembic commands ###

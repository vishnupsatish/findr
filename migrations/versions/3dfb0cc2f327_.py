"""empty message

Revision ID: 3dfb0cc2f327
Revises: 
Create Date: 2020-06-10 12:36:15.467530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dfb0cc2f327'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('store', sa.Column('address', sa.String(), nullable=True))
    op.add_column('store', sa.Column('chain', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('store', 'chain')
    op.drop_column('store', 'address')
    # ### end Alembic commands ###

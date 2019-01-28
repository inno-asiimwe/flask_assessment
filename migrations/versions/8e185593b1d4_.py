"""empty message

Revision ID: 8e185593b1d4
Revises: cb3133819916
Create Date: 2019-01-28 13:41:50.724400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e185593b1d4'
down_revision = 'cb3133819916'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('breed', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('color', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['breed'], ['breeds.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dogs')
    # ### end Alembic commands ###

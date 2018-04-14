"""empty message

Revision ID: 0f11d987740a
Revises: a4d7a4a91260
Create Date: 2018-04-10 16:04:00.133174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f11d987740a'
down_revision = 'a4d7a4a91260'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('status', sa.Integer(), nullable=True))
    op.add_column('post', sa.Column('views', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'views')
    op.drop_column('post', 'status')
    # ### end Alembic commands ###
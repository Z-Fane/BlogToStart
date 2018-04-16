"""empty message

Revision ID: 3eb3eee7cf5e
Revises: a2d62f53b8f8
Create Date: 2018-04-15 21:54:54.918046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eb3eee7cf5e'
down_revision = 'a2d62f53b8f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tag', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tag', type_='unique')
    # ### end Alembic commands ###

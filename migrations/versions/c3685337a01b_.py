"""empty message

Revision ID: c3685337a01b
Revises: 51f3a2ffd8fa
Create Date: 2024-09-30 22:02:27.587272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3685337a01b'
down_revision = '51f3a2ffd8fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thumbnail_url', sa.Text(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_column('thumbnail_url')

    # ### end Alembic commands ###

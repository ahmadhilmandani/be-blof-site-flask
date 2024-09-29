"""empty message

Revision ID: 51f3a2ffd8fa
Revises: d2367222c3cd
Create Date: 2024-09-30 05:12:01.338168

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '51f3a2ffd8fa'
down_revision = 'd2367222c3cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.TIMESTAMP(), nullable=True))
        batch_op.drop_column('like')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('like', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###

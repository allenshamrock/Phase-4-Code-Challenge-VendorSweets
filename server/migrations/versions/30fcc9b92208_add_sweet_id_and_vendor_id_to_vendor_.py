"""Add sweet_id and vendor_id to vendor_sweets table

Revision ID: 30fcc9b92208
Revises: ed0a2ac3b9a5
Create Date: 2024-04-15 15:09:08.873176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30fcc9b92208'
down_revision = 'ed0a2ac3b9a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vendor_sweets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sweet_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('vendor_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_vendor_sweets_sweet_id_sweets'), 'sweets', ['sweet_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_vendor_sweets_vendor_id_vendors'), 'vendors', ['vendor_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vendor_sweets', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_vendor_sweets_vendor_id_vendors'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_vendor_sweets_sweet_id_sweets'), type_='foreignkey')
        batch_op.drop_column('vendor_id')
        batch_op.drop_column('sweet_id')

    # ### end Alembic commands ###

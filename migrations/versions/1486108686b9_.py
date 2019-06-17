"""empty message

Revision ID: 1486108686b9
Revises: 
Create Date: 2019-06-17 16:03:00.142322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1486108686b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manufacturer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('street', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('zip', sa.String(length=10), nullable=True),
    sa.Column('country', sa.String(length=24), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('micro_processor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=25), nullable=False),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('raw_data',
    sa.Column('data_id', sa.Integer(), nullable=False),
    sa.Column('time_stamp', sa.DateTime(), nullable=True),
    sa.Column('value', sa.Text(), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('data_id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('roll_id', sa.Integer(), nullable=True),
    sa.Column('reset_token', sa.Text(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('vendor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('street', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('zip', sa.String(length=10), nullable=True),
    sa.Column('country', sa.String(length=24), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('board',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('microprocessor_id', sa.Integer(), nullable=True),
    sa.Column('secret', sa.String(length=64), nullable=False),
    sa.Column('prime_location', sa.String(length=3), nullable=True),
    sa.Column('location', sa.String(length=50), nullable=True),
    sa.Column('sub_location', sa.String(length=20), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.Column('manufacturer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturer.id'], ),
    sa.ForeignKeyConstraint(['microprocessor_id'], ['micro_processor.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('component',
    sa.Column('component_id', sa.Integer(), nullable=False),
    sa.Column('component_name', sa.String(length=120), nullable=True),
    sa.Column('purpose', sa.String(length=120), nullable=True),
    sa.Column('manufacturer_id', sa.String(length=64), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.Column('price_paid', sa.Float(), nullable=True),
    sa.Column('date_purchased', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('pin_no', sa.Integer(), nullable=True),
    sa.Column('MQTT_topic', sa.String(length=120), nullable=True),
    sa.Column('usage', sa.Text(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturer.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendor.id'], ),
    sa.PrimaryKeyConstraint('component_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('component')
    op.drop_table('board')
    op.drop_table('vendor')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('raw_data')
    op.drop_table('micro_processor')
    op.drop_table('manufacturer')
    # ### end Alembic commands ###

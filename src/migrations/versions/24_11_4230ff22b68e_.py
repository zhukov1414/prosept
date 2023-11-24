"""empty message

Revision ID: 4230ff22b68e
Revises: 
Create Date: 2023-11-24 15:18:46.498210

"""
from typing import Sequence, Union

from alembic import op
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4230ff22b68e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dealer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('article', sa.String(), nullable=False),
    sa.Column('ean_13', sa.Float(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.Column('recommended_price', sa.String(), nullable=True),
    sa.Column('category_id', sa.Float(), nullable=True),
    sa.Column('ozon_name', sa.String(), nullable=True),
    sa.Column('name_1c', sa.String(), nullable=True),
    sa.Column('wb_name', sa.String(), nullable=True),
    sa.Column('ozon_article', sa.Float(), nullable=True),
    sa.Column('wb_article', sa.Float(), nullable=True),
    sa.Column('ym_article', sa.String(), nullable=True),
    sa.Column('wb_article_td', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('dealerprice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_key', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('product_url', sa.String(), nullable=True),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('dealer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dealer_id'], ['dealer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_key')
    )
    op.create_table('productdealer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('dealer_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dealer_id'], ['dealer.id'], ),
    sa.ForeignKeyConstraint(['key'], ['dealerprice.product_key'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('productdealer')
    op.drop_table('dealerprice')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('product')
    op.drop_table('dealer')
    # ### end Alembic commands ###

"""empty message

Revision ID: 7b5152d18ece
Revises: 
Create Date: 2017-09-19 20:06:23.039271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b5152d18ece'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=10), nullable=True),
    sa.Column('password', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_nickname'), 'user', ['nickname'], unique=True)
    op.create_table('folder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('parent', sa.String(length=64), nullable=True),
    sa.Column('url', sa.String(length=1024), nullable=True),
    sa.Column('path', sa.String(length=1024), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_folder_name'), 'folder', ['name'], unique=False)
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=128), nullable=True),
    sa.Column('inner_link', sa.String(length=1024), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('folder_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['folder_id'], ['folder.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_file_name'), 'file', ['file_name'], unique=False)
    op.create_index(op.f('ix_file_inner_link'), 'file', ['inner_link'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_file_inner_link'), table_name='file')
    op.drop_index(op.f('ix_file_file_name'), table_name='file')
    op.drop_table('file')
    op.drop_index(op.f('ix_folder_name'), table_name='folder')
    op.drop_table('folder')
    op.drop_index(op.f('ix_user_nickname'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###

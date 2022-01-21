"""empty message

Revision ID: 6277e53fcc9f
Revises: 
Create Date: 2022-01-20 19:51:22.583169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6277e53fcc9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('colaborador',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('anonymus', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('destacados',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('colaborador', sa.String(length=200), nullable=False),
    sa.Column('colab_id', sa.Integer(), nullable=False),
    sa.Column('organizacion', sa.String(length=200), nullable=False),
    sa.Column('org_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('colab_id'),
    sa.UniqueConstraint('colaborador'),
    sa.UniqueConstraint('org_id'),
    sa.UniqueConstraint('organizacion')
    )
    op.create_table('login',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('user_type', sa.Enum('ORGANIZACION', 'PARTICULAR', 'CORPORATIVO', name='tipousuario'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password')
    )
    op.create_table('organizacion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_name', sa.String(length=200), nullable=False),
    sa.Column('rif', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=False),
    sa.Column('person', sa.String(length=200), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('org_name'),
    sa.UniqueConstraint('person'),
    sa.UniqueConstraint('rif')
    )
    op.create_table('colaboracion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('colaborador', sa.String(length=200), nullable=False),
    sa.Column('colab_id', sa.Integer(), nullable=False),
    sa.Column('organizacion', sa.String(length=200), nullable=False),
    sa.Column('org_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['org_id'], ['organizacion.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('colab_id'),
    sa.UniqueConstraint('colaborador'),
    sa.UniqueConstraint('org_id'),
    sa.UniqueConstraint('organizacion')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('colaboracion')
    op.drop_table('organizacion')
    op.drop_table('login')
    op.drop_table('destacados')
    op.drop_table('colaborador')
    # ### end Alembic commands ###
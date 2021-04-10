"""empty message

Revision ID: 39b113af8558
Revises: 
Create Date: 2021-04-10 16:14:25.583517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39b113af8558'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('PeopleRelationship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('father_id', sa.Integer(), nullable=True),
    sa.Column('mother_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['father_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['mother_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('PeopleRelationship')
    op.drop_table('person')
    # ### end Alembic commands ###
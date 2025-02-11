"""Add question_id to response

Revision ID: 97261766f7f8
Revises: 
Create Date: 2025-01-14 23:25:01.815657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97261766f7f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('response', schema=None) as batch_op:
        batch_op.add_column(sa.Column('question_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'question', ['question_id'], ['id'])
        batch_op.drop_column('survey_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('response', schema=None) as batch_op:
        batch_op.add_column(sa.Column('survey_id', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'survey', ['survey_id'], ['id'])
        batch_op.drop_column('question_id')

    # ### end Alembic commands ###

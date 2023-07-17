"""add reader_id column in books table for one-to-one relationship

Revision ID: 41ee718d3f2a
Revises: 58469b2979de
Create Date: 2023-07-17 17:36:40.944239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41ee718d3f2a'
down_revision = '58469b2979de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('readers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('books', sa.Column('reader_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_books_reader_id'), 'books', ['reader_id'], unique=False)
    op.create_foreign_key(None, 'books', 'readers', ['reader_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_index(op.f('ix_books_reader_id'), table_name='books')
    op.drop_column('books', 'reader_id')
    op.drop_table('readers')
    # ### end Alembic commands ###

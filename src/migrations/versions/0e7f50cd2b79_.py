"""empty message

Revision ID: 0e7f50cd2b79
Revises: dc2c75747e1b
Create Date: 2023-11-16 14:13:40.988273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e7f50cd2b79'
down_revision: Union[str, None] = 'dc2c75747e1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userMissions', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('userMissions', sa.Column('modified_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('userMissions', 'modified_at')
    op.drop_column('userMissions', 'created_at')
    # ### end Alembic commands ###

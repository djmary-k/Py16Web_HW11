"""init

Revision ID: a2eb6daa4fcd
Revises: 1df73be2338f
Create Date: 2024-01-05 01:42:50.286482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2eb6daa4fcd'
down_revision: Union[str, None] = '1df73be2338f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contacts', 'extra_data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('extra_data', sa.VARCHAR(length=150), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

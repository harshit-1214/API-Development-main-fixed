"""create posts table

Revision ID: 8af73da9fd1d
Revises: 
Create Date: 2026-09-28 12:04:17.545868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8af73da9fd1d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('post', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title' , sa.String(), nullable=False))
   
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('post')
    pass

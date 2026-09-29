"""add content column to post

Revision ID: 3317c4ec97be
Revises: 330e6c121fd0
Create Date: 2026-09-28 12:41:45.330260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3317c4ec97be'
down_revision: Union[str, Sequence[str], None] = '8af73da9fd1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

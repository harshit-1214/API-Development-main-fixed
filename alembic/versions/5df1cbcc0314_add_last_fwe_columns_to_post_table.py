"""add last fwe columns to post table

Revision ID: 5df1cbcc0314
Revises: 4161ea502697
Create Date: 2026-09-28 13:46:28.374649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5df1cbcc0314'
down_revision: Union[str, Sequence[str], None] = '4161ea502697'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post', sa.Column(
        'published', sa.Boolean(),nullable=False, server_default='TRUE'))
    op.add_column('post', sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')

    pass

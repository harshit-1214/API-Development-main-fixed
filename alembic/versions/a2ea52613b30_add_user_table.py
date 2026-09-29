"""add user table

Revision ID: a2ea52613b30
Revises: 3317c4ec97be
Create Date: 2026-09-28 12:55:33.388476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2ea52613b30'
down_revision: Union[str, Sequence[str], None] = '3317c4ec97be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('user',
                    sa.Column('id', sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                    server_default=sa.text('now()'),nullable=False ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""add foregin-key to post table

Revision ID: 4161ea502697
Revises: a2ea52613b30
Create Date: 2026-09-28 13:17:07.746151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4161ea502697'
down_revision: Union[str, Sequence[str], None] = 'a2ea52613b30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post' , sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk', source_table="post", referent_table="user",
                          local_cols=['owner_id'], remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name='post')
    op.drop_column('post', 'owner_id')
    pass

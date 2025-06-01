"""create post table

Revision ID: 0e47d63efe14
Revises: 
Create Date: 2025-06-01 00:47:23.036921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e47d63efe14'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("posts",sa.Column('id',sa.Integer(), primary_key=True, nullable=False), sa.Column('title', sa.String(), nullable=False), sa.Column('content', sa.String(), nullable=False), sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False))
    """Upgrade schema."""
    pass


def downgrade():
    op.drop_table("posts")
    """Downgrade schema."""
    pass

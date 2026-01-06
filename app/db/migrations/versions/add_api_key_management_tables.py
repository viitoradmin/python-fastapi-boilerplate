"""Add API key management tables

Revision ID: api_key_001
Revises: d25b402640b5
Create Date: 2025-01-05 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'api_key_001'
down_revision: Union[str, Sequence[str], None] = 'd25b402640b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create api_keys table
    op.create_table('api_keys',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('key_hash', sa.String(length=255), nullable=False),
        sa.Column('key_prefix', sa.String(length=20), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('scopes', sa.Text(), nullable=True),
        sa.Column('allowed_ips', sa.Text(), nullable=True),
        sa.Column('rate_limit', sa.Integer(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('idx_api_key_hash', 'api_keys', ['key_hash'], unique=True)
    op.create_index('idx_api_key_prefix', 'api_keys', ['key_prefix'], unique=False)
    op.create_index('idx_api_key_user_id', 'api_keys', ['user_id'], unique=False)
    op.create_index('idx_api_key_active', 'api_keys', ['is_active'], unique=False)
    op.create_index('idx_api_key_expires', 'api_keys', ['expires_at'], unique=False)
    op.create_index('idx_api_key_user_active', 'api_keys', ['user_id', 'is_active'], unique=False)
    op.create_index(op.f('ix_api_keys_id'), 'api_keys', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index(op.f('ix_api_keys_id'), table_name='api_keys')
    op.drop_index('idx_api_key_user_active', table_name='api_keys')
    op.drop_index('idx_api_key_expires', table_name='api_keys')
    op.drop_index('idx_api_key_active', table_name='api_keys')
    op.drop_index('idx_api_key_user_id', table_name='api_keys')
    op.drop_index('idx_api_key_prefix', table_name='api_keys')
    op.drop_index('idx_api_key_hash', table_name='api_keys')
    
    # Drop table
    op.drop_table('api_keys')
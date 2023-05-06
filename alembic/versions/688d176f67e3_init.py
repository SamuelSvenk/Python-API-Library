"""init

Revision ID: 688d176f67e3
Revises: 
Create Date: 2023-05-05 16:47:49.111831

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '688d176f67e3'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():

    card_status = postgresql.ENUM('active', 'inactive', 'expired', name='card_status')

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(as_uuid=True),primary_key=True, default=uuid4),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("surname", sa.String , nullable=False),
        sa.Column("email", sa.String(254), unique=False, nullable=False),
        sa.Column("birth_date", sa.DateTime, nullable=False),
        sa.Column("personal_identificator", sa.String, unique=True, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.Column("is_childuser", sa.Boolean, nullable=False),
    )

    op.create_table(
        "cards",
        sa.Column("id", sa.UUID(as_uuid=True),primary_key=True, default=uuid4),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("magstripe", sa.String(20), nullable=False),
        sa.Column("status", card_status, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        )
    

def downgrade():
    op.drop_table("users")
    op.drop_table("cards")
    card_status = postgresql.ENUM('active', 'inactive', 'expired', name='card_status')
    card_status.drop(op.get_bind(), checkfirst=False)

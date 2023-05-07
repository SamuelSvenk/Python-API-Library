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
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '688d176f67e3'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():

    card_status = postgresql.ENUM('active', 'inactive', 'expired', name='card_status')
    instance_type = postgresql.ENUM('physical', 'ebook', 'audiobook', name='instance_type')
    instance_status = postgresql.ENUM('available', 'inactive', name='instance_status')
    rental_status = postgresql.ENUM('active', 'returned', name='rental_status')

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(as_uuid=True),primary_key=True, default=uuid4, unique=True, nullable=False),
        sa.Column("name", sa.String, nullable=True),
        sa.Column("surname", sa.String , nullable=True),
        sa.Column("email", sa.String(254), unique=False, nullable=True),
        sa.Column("birth_date", sa.Date, nullable=True),
        sa.Column("personal_identificator", sa.String, unique=True, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.Column("is_childuser", sa.Boolean, nullable=True),
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
    
    op.create_table(
        "authors",
        sa.Column("id", sa.UUID(as_uuid=True),primary_key=True, default=uuid4),
        sa.Column("name", sa.String, nullable=True),
        sa.Column("surname", sa.String , nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.UUID(as_uuid=True),primary_key=True, default=uuid4),
        sa.Column("name", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "publications",
        sa.Column("id", sa.UUID(as_uuid=True),primary_key=True, default=uuid4),
        sa.Column("title", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "publications_authors",
        sa.Column("publication_id", sa.UUID, sa.ForeignKey("publications.id"), nullable=True),
        sa.Column("author_id", sa.UUID, sa.ForeignKey("authors.id"), nullable=True),

    )

    op.create_table(
        "publications_categories",
        sa.Column("publication_id", sa.UUID, sa.ForeignKey("publications.id"), nullable=True),
        sa.Column("category_id", sa.UUID, sa.ForeignKey("categories.id"), nullable=True),
    )

    op.create_table(
        "instances",
        sa.Column("id", sa.UUID(as_uuid=True),primary_key=True, default=uuid4),
        sa.Column("type", instance_type, nullable=False),
        sa.Column("publisher", sa.String, nullable=True),
        sa.Column("year", sa.Integer, nullable=True),
        sa.Column("status", instance_status, nullable=False),
        sa.Column("publication_id", sa.UUID, sa.ForeignKey("publications.id"), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "rentals",
        sa.Column("id", sa.UUID(as_uuid=True),primary_key=True, default=uuid4),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("publication_id", sa.UUID, sa.ForeignKey("publications.id"), nullable=False),
        sa.Column("instance_id", sa.UUID, sa.ForeignKey("instances.id"), nullable=False),
        sa.Column("status", rental_status, nullable=True),
        sa.Column("duration", sa.Integer, nullable=True),
        sa.Column("start_date", sa.DateTime, nullable=True),
        sa.Column("end_date", sa.DateTime, nullable=True),

    )
    op.create_table(
        "reservations",
        sa.Column("id", sa.UUID(as_uuid=True),primary_key=True, default=uuid4),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("publication_id", sa.UUID, sa.ForeignKey("publications.id"), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True)
    )


    
def downgrade():
    op.drop_table("users")
    op.drop_table("cards")
    op.drop_table("authors")
    op.drop_table("categories")
    op.drop_table("publications_authors")
    op.drop_table("publications_categories")
    op.drop_table("instances")
    op.drop_table("rentals")
    op.drop_table("reservations")
    op.drop_table("publications")
    card_status = postgresql.ENUM('active', 'inactive', 'expired', name='card_status')
    instance_type = postgresql.ENUM('physical', 'ebook', 'audiobook', name='instance_type')
    instance_status = postgresql.ENUM('available', 'inactive', name='instance_status')
    rental_status = postgresql.ENUM('active', 'returned', name='rental_status')
    instance_type.drop(op.get_bind(), checkfirst=False)
    instance_status.drop(op.get_bind(), checkfirst=False)
    rental_status.drop(op.get_bind(), checkfirst=False)
    card_status.drop(op.get_bind(), checkfirst=False)


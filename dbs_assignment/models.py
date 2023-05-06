from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.sql.schema import Column
from dbs_assignment.database import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    birth_date = Column(DateTime, nullable=False)
    personal_identificator = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    is_childuser = Column(Boolean, nullable=False)
    cards = relationship("Card", back_populates="user")



class Card(Base):
    __tablename__ = "cards"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    magstripe = Column(String(20), unique=True, nullable=False)
    status = Column(postgresql.ENUM("active", "expired", "inactive", name="cardstatus"), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="cards")
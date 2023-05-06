from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, Boolean, Float, Date
from sqlalchemy.sql.schema import Column
from dbs_assignment.database import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4, unique=True, nullable=False)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String(254), unique=True, nullable=True)
    birth_date = Column(Date, nullable=True)
    personal_identificator = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    is_childuser = Column(Boolean, nullable=False)
    cards = relationship("Card", back_populates="user")
    rentals = relationship("Rental", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")

class Card(Base):
    __tablename__ = "cards"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    magstripe = Column(String(20), unique=True, nullable=False)
    status = Column(postgresql.ENUM("active", "expired", "inactive", name="cardstatus"), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="cards")

class Author(Base):
    __tablename__ = "authors"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4)
    name = Column(String, nullable=True)
    surname = Column(String , nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    publications = relationship('Publication', secondary='publications_authors', back_populates='authors')

class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    publications = relationship('Publication', secondary='publications_categories', back_populates='categories')


class Publication(Base):
    __tablename__ = "publications"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4)
    title = Column(String, nullable=True)
    authors = relationship('Author', secondary='publications_authors', back_populates='publications')
    categories = relationship('Category', secondary='publications_categories', back_populates='publications')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    instances = relationship("Instance", back_populates="publication")
    rentals = relationship("Rental", back_populates="publication")
    reservations = relationship("Reservation", back_populates="publication")


class PublicationAuthor(Base):
    __tablename__ = 'publications_authors'
    publication_id = Column(UUID(as_uuid=True), ForeignKey('publications.id'), primary_key=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.id'), primary_key=True)

    
class PublicationCategory(Base):
    __tablename__ = 'publications_categories'
    publication_id = Column(UUID(as_uuid=True), ForeignKey('publications.id'), primary_key=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), primary_key=True)


class Instance(Base):
    __tablename__ = "instances"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4)
    publication_id = Column(UUID, ForeignKey("publications.id"), nullable=False)
    status = Column(postgresql.ENUM("available", "reserved", name="instancestatus"), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    publication = relationship("Publication", back_populates="instances")

class Rental(Base):
    __tablename__ = "rentals"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4)
    publication_id = Column(UUID, ForeignKey("publications.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    publication = relationship("Publication", back_populates="rentals")
    user = relationship("User", back_populates="rentals")

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid4)
    publication_id = Column(UUID, ForeignKey("publications.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    publication = relationship("Publication", back_populates="reservations")
    user = relationship("User", back_populates="reservations")



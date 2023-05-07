from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dbs_assignment.config import settings
from sqlalchemy.pool import QueuePool

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, poolclass=QueuePool,pool_size=10,max_overflow=20, pool_pre_ping=True, pool_timeout=300)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()

def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
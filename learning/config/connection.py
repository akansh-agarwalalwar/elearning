from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import config
from database.models import Base

# Create sync engine
engine = create_engine(config.DATABASE_URL, echo=True)

# Create sync session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
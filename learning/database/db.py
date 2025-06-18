from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.config import config

# Create base class for models
Base = declarative_base()

# Create sync engine
engine = create_engine(config.DATABASE_URL, echo=True)

# Create sync session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    Base.metadata.create_all(bind=engine)

# Close database connection
def close_db():
    engine.dispose() 
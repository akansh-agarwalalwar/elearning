import logging
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import User
from config.connection import get_db

logger = logging.getLogger(__name__)

def get_user(email: str, session: Session):
    logger.debug("Fetching user from database", extra={"email": email})
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user
    return None
    
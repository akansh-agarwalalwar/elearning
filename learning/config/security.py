import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import User
from database.db import get_session

logger = logging.getLogger(__name__)

async def get_user(email: str, session: AsyncSession = get_session()):
    logger.debug("Fetching user from database", extra={"email": email})
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user:
        return user
    return None
    
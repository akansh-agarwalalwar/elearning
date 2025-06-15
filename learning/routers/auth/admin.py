from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_session
from database.models import BaseUser, Admin, Student, Instructor
from models.user import BaseUserIn, BaseUser as BaseUserPydantic
from services.authservice import hash_password

router = APIRouter()

@router.post("/create-user", response_model=BaseUserPydantic, status_code=status.HTTP_201_CREATED)
async def register(user_in: BaseUserIn, session: AsyncSession = Depends(get_session)):
    # Check if username or email already exists
    query = select(BaseUser).where(
        (BaseUser.username == user_in.username) | (BaseUser.email == user_in.email)
    )
    result = await session.execute(query)
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    hashed_password = hash_password(user_in.password)
    
    # Create base user
    new_base_user = BaseUser(
        username=user_in.username,
        password=hashed_password,
        email=user_in.email,
        user_type=user_in.user_type
    )
    
    session.add(new_base_user)
    await session.flush()  # Flush to get the base_user_id
    
    # Create role-specific user
    if user_in.user_type == "admin":
        new_role_user = Admin(base_user_id=new_base_user.id)
    elif user_in.user_type == "student":
        new_role_user = Student(base_user_id=new_base_user.id)
    elif user_in.user_type == "instructor":
        new_role_user = Instructor(base_user_id=new_base_user.id)
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")
    
    session.add(new_role_user)
    await session.commit()
    await session.refresh(new_base_user)
    
    return BaseUserPydantic.from_orm(new_base_user)

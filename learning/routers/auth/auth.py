from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_session
from database.models import BaseUser
from models.user import BaseUserIn, BaseUser as BaseUserPydantic
from services.authservice import hash_password, verify_password, create_access_token
from datetime import timedelta
from middleware.auth import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=BaseUserPydantic, status_code=status.HTTP_201_CREATED)
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
    await session.commit()
    await session.refresh(new_base_user)
    
    return BaseUserPydantic.from_orm(new_base_user)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    # Find user by username
    query = select(BaseUser).where(BaseUser.username == form_data.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username, "user_type": user.user_type},
        expires_delta=timedelta(minutes=30)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user.user_type,
        "username":user.username
    }

@router.get("/me", response_model=BaseUserPydantic)
async def get_current_user_info(current_user: BaseUser = Depends(get_current_user)):
    return BaseUserPydantic.from_orm(current_user)

@router.get("/get-users", response_model=list[BaseUserPydantic])
async def get_users(session: AsyncSession = Depends(get_session)):
    query = select(BaseUser)
    result = await session.execute(query)
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=400, detail="No user found in database")
    return [BaseUserPydantic.from_orm(user) for user in users]

@router.delete("/delete-user")
async def delete_user(email: str = Query(...), session: AsyncSession = Depends(get_session)):
    query = select(BaseUser).where(BaseUser.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}
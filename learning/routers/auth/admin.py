from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from config.connection import get_db
from database.models import User
from utils.enums import UserRole
from services.authservice import hash_password
from services.privilege_service import PrivilegeService
from middleware.auth import get_current_admin
from pydantic import BaseModel

router = APIRouter()

class AdminUserCreateRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/create-user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: AdminUserCreateRequest, 
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new user (Admin only)
    """
    # Check if username or email already exists
    existing = db.query(User).filter(
        (User.username == user_in.username) | (User.email == user_in.email)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Validate role
    try:
        role = UserRole(user_in.role.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user role")

    hashed_password = hash_password(user_in.password)
    
    # Create user
    new_user = User(
        username=user_in.username,
        password=hashed_password,
        email=user_in.email,
        role=role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Assign default privileges if instructor
    if role == UserRole.INSTRUCTOR:
        privilege_service = PrivilegeService(db)
        privilege_service.assign_default_privileges_to_instructor(
            instructor_id=new_user.id,
            admin_id=current_admin.id
        )
    
    return new_user

@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all users (Admin only)
    """
    users = db.query(User).all()
    return users

@router.get("/users/{role}", response_model=list[UserResponse])
async def get_users_by_role(
    role: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get users by role (Admin only)
    """
    try:
        user_role = UserRole(role.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user role")
    
    users = db.query(User).filter(User.role == user_role).all()
    return users

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Delete a user (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deleting themselves
    if user.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

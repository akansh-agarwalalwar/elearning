from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from config.connection import get_db
from database.models import User
from middleware.auth import get_current_user
from middleware.privilege_checker import check_privilege, get_user_privileges
from utils.enums import UserRole
from pydantic import BaseModel

router = APIRouter()

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True

@router.get("/profile", response_model=UserProfileResponse)
async def get_instructor_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current instructor's profile information.
    """
    if current_user.role != UserRole.INSTRUCTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can access this endpoint"
        )
    
    return current_user

@router.get("/dashboard")
async def get_instructor_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get instructor dashboard statistics.
    """
    if current_user.role != UserRole.INSTRUCTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can access this endpoint"
        )
    
    # Get course count for the instructor
    from database.models import Course, Enrollment
    from sqlalchemy import func
    
    # Count courses
    course_count = db.query(func.count(Course.id)).filter(
        Course.instructor_id == current_user.id,
        Course.is_active == True
    ).scalar()
    
    # Count total enrollments across all instructor's courses
    enrollment_count = db.query(func.count(Enrollment.id)).join(
        Course, Enrollment.course_id == Course.id
    ).filter(
        Course.instructor_id == current_user.id,
        Course.is_active == True,
        Enrollment.is_active == True
    ).scalar()
    
    # Get user privileges
    privileges = get_user_privileges(current_user, db)
    
    return {
        "instructor_id": current_user.id,
        "total_courses": course_count,
        "total_enrollments": enrollment_count,
        "privileges": privileges,
        "message": "Instructor dashboard data retrieved successfully"
    }

@router.get("/privileges")
async def get_my_privileges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current instructor's privileges
    """
    if current_user.role != UserRole.INSTRUCTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can access this endpoint"
        )
    
    privileges = get_user_privileges(current_user, db)
    
    return {
        "instructor_id": current_user.id,
        "privileges": privileges,
        "message": "Privileges retrieved successfully"
    }
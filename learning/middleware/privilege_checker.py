from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.connection import get_db
from services.privilege_service import PrivilegeService
from middleware.auth import get_current_user
from database.models import User
from functools import wraps

def require_privilege(privilege_name: str):
    """
    Decorator to check if an instructor has a specific privilege
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get current user and db from kwargs or dependencies
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user or not db:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="User or database session not available"
                )
            
            # Allow admins to bypass privilege checks
            if current_user.role == "admin":
                return func(*args, **kwargs)
            
            # For instructors, check if they have the required privilege
            if current_user.role == "instructor":
                privilege_service = PrivilegeService(db)
                has_privilege = privilege_service.check_instructor_privilege(
                    instructor_id=current_user.id,
                    privilege_name=privilege_name
                )
                
                if not has_privilege:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Instructor does not have the required privilege: {privilege_name}"
                    )
                
                return func(*args, **kwargs)
            
            # For students, deny access
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students cannot access this resource"
            )
        
        return wrapper
    return decorator

def check_privilege(privilege_name: str, current_user: User, db: Session) -> bool:
    """
    Utility function to check if a user has a specific privilege
    """
    # Admins have all privileges
    if current_user.role == "admin":
        return True
    
    # For instructors, check the privilege
    if current_user.role == "instructor":
        privilege_service = PrivilegeService(db)
        return privilege_service.check_instructor_privilege(
            instructor_id=current_user.id,
            privilege_name=privilege_name
        )
    
    # Students have no privileges
    return False

def get_user_privileges(current_user: User, db: Session) -> list:
    """
    Get all privileges for the current user
    """
    if current_user.role == "admin":
        return ["all_privileges"]  # Admins have all privileges
    
    if current_user.role == "instructor":
        privilege_service = PrivilegeService(db)
        privileges = privilege_service.get_instructor_privileges(current_user.id)
        return [p.privilege_name for p in privileges]
    
    return []  # Students have no privileges 
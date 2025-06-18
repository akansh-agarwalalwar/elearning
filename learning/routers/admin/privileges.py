from fastapi import APIRouter, Depends, HTTPException, status
from config.connection import get_db
from sqlalchemy.orm import Session
from services.privilege_service import PrivilegeService
from middleware.auth import get_current_user
from database.models import User
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/admin/privileges", tags=["Admin Privileges"])

class PrivilegeAssignRequest(BaseModel):
    instructor_id: int
    privilege_name: str
    privilege_description: str

class PrivilegeRevokeRequest(BaseModel):
    instructor_id: int
    privilege_name: str

class PrivilegeResponse(BaseModel):
    id: int
    instructor_id: int
    privilege_name: str
    privilege_description: str
    is_active: bool
    assigned_by: int
    assigned_at: str
    
    class Config:
        from_attributes = True

@router.post("/assign", response_model=PrivilegeResponse)
async def assign_privilege(
    request: PrivilegeAssignRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Assign a privilege to an instructor (Admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can assign privileges"
        )
    
    privilege_service = PrivilegeService(db)
    
    try:
        privilege = privilege_service.assign_privilege_to_instructor(
            instructor_id=request.instructor_id,
            privilege_name=request.privilege_name,
            privilege_description=request.privilege_description,
            admin_id=current_user.id
        )
        return privilege
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/revoke")
async def revoke_privilege(
    request: PrivilegeRevokeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Revoke a privilege from an instructor (Admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can revoke privileges"
        )
    
    privilege_service = PrivilegeService(db)
    
    try:
        success = privilege_service.revoke_privilege_from_instructor(
            instructor_id=request.instructor_id,
            privilege_name=request.privilege_name,
            admin_id=current_user.id
        )
        return {"message": "Privilege revoked successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/instructor/{instructor_id}", response_model=List[PrivilegeResponse])
async def get_instructor_privileges(
    instructor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all privileges for a specific instructor (Admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view instructor privileges"
        )
    
    privilege_service = PrivilegeService(db)
    privileges = privilege_service.get_instructor_privileges(instructor_id)
    return privileges

@router.get("/all", response_model=List[PrivilegeResponse])
async def get_all_privileges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all privileges (Admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view all privileges"
        )
    
    privilege_service = PrivilegeService(db)
    privileges = privilege_service.get_all_privileges()
    return privileges

@router.get("/my-assignments", response_model=List[PrivilegeResponse])
async def get_privileges_assigned_by_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all privileges assigned by the current admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view their privilege assignments"
        )
    
    privilege_service = PrivilegeService(db)
    privileges = privilege_service.get_privileges_by_admin(current_user.id)
    return privileges 
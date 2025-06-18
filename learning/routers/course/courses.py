from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from config.connection import get_db
from services.course_service import CourseService
from middleware.auth import get_current_user
from middleware.privilege_checker import check_privilege
from database.models import User
from utils.enums import PrivilegeName, UserRole, CourseStatus
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/courses", tags=["Courses"])

# Pydantic models
class CourseCreateRequest(BaseModel):
    title: str
    description: str
    fee: int = 0
    banner_image: Optional[str] = None

class CourseUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    fee: Optional[int] = None
    banner_image: Optional[str] = None
    status: Optional[str] = None

class DiscountRequest(BaseModel):
    discounted_fee: int
    start_date: datetime
    end_date: datetime

class CourseResponse(BaseModel):
    id: str
    title: str
    description: str
    instructor_id: int
    banner_image: Optional[str]
    fee: int
    discounted_fee: Optional[int]
    discount_start_date: Optional[datetime]
    discount_end_date: Optional[datetime]
    total_enrolled: int
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CourseStatisticsResponse(BaseModel):
    course_id: str
    title: str
    status: str
    status_description: str
    total_enrollments: int
    recent_enrollments_30_days: int
    fee_information: dict
    created_at: datetime
    updated_at: datetime

@router.post("/", response_model=CourseResponse)
async def create_course(
    course_data: CourseCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new course (Instructor with create_course privilege or Admin)
    """
    if current_user.role == UserRole.INSTRUCTOR:
        if not check_privilege(PrivilegeName.CREATE_COURSE.value, current_user, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Instructor does not have permission to create courses"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can create courses"
        )
    
    course_service = CourseService(db)
    
    # Generate course ID (you might want to use UUID or other ID generation)
    import uuid
    course_id = str(uuid.uuid4())
    
    course_data_dict = course_data.dict()
    course_data_dict["id"] = course_id
    course_data_dict["instructor_id"] = current_user.id
    
    try:
        course = course_service.create_course(course_data_dict)
        return course
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    status: Optional[str] = Query(None, description="Filter by course status"),
    min_fee: Optional[int] = Query(None, description="Minimum fee filter"),
    max_fee: Optional[int] = Query(None, description="Maximum fee filter"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get courses with optional filters
    """
    course_service = CourseService(db)
    
    try:
        # Convert status string to enum if provided
        status_enum = None
        if status:
            try:
                status_enum = CourseStatus(status)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status: {status}"
                )
        
        courses = course_service.search_courses(
            query=search,
            status=status_enum,
            min_fee=min_fee,
            max_fee=max_fee
        )
        return courses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/enrollable", response_model=List[CourseResponse])
async def get_enrollable_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all courses that students can enroll in
    """
    course_service = CourseService(db)
    courses = course_service.get_enrollable_courses()
    return courses

@router.get("/my-courses", response_model=List[CourseResponse])
async def get_my_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get courses created by the current instructor
    """
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can view their courses"
        )
    
    course_service = CourseService(db)
    courses = course_service.get_courses_by_instructor(current_user.id)
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific course by ID
    """
    course_service = CourseService(db)
    
    try:
        course = course_service.get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        return course
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course_data: CourseUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a course (Course owner or Admin)
    """
    course_service = CourseService(db)
    
    # Check if course exists and user has permission
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == UserRole.INSTRUCTOR:
        if course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own courses"
            )
        if not check_privilege(PrivilegeName.EDIT_COURSE.value, current_user, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Instructor does not have permission to edit courses"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can update courses"
        )
    
    try:
        # Remove None values from the update data
        update_data = {k: v for k, v in course_data.dict().items() if v is not None}
        
        # Convert status string to enum if provided
        if 'status' in update_data:
            try:
                update_data['status'] = CourseStatus(update_data['status'])
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status: {update_data['status']}"
                )
        
        updated_course = course_service.update_course(course_id, update_data)
        return updated_course
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{course_id}/discount")
async def set_course_discount(
    course_id: str,
    discount_data: DiscountRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set discount for a course (Course owner or Admin)
    """
    course_service = CourseService(db)
    
    # Check permissions
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == UserRole.INSTRUCTOR:
        if course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only set discounts for your own courses"
            )
        if not check_privilege(PrivilegeName.SET_DISCOUNTS.value, current_user, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Instructor does not have permission to set discounts"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can set course discounts"
        )
    
    try:
        updated_course = course_service.set_course_discount(
            course_id,
            discount_data.discounted_fee,
            discount_data.start_date,
            discount_data.end_date
        )
        return {"message": "Discount set successfully", "course": updated_course}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{course_id}/discount")
async def remove_course_discount(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove discount from a course (Course owner or Admin)
    """
    course_service = CourseService(db)
    
    # Check permissions
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == UserRole.INSTRUCTOR:
        if course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only remove discounts from your own courses"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can remove course discounts"
        )
    
    try:
        updated_course = course_service.remove_course_discount(course_id)
        return {"message": "Discount removed successfully", "course": updated_course}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{course_id}/publish")
async def publish_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Publish a course (Course owner or Admin)
    """
    course_service = CourseService(db)
    
    # Check permissions
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == UserRole.INSTRUCTOR:
        if course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only publish your own courses"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can publish courses"
        )
    
    try:
        updated_course = course_service.publish_course(course_id)
        return {"message": "Course published successfully", "course": updated_course}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{course_id}/archive")
async def archive_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Archive a course (Course owner or Admin)
    """
    course_service = CourseService(db)
    
    # Check permissions
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == UserRole.INSTRUCTOR:
        if course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only archive your own courses"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can archive courses"
        )
    
    try:
        updated_course = course_service.archive_course(course_id)
        return {"message": "Course archived successfully", "course": updated_course}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{course_id}/submit-review")
async def submit_course_for_review(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a course for admin review (Course owner only)
    """
    course_service = CourseService(db)
    
    # Check permissions
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == UserRole.INSTRUCTOR:
        if course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only submit your own courses for review"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can submit courses for review"
        )
    
    try:
        updated_course = course_service.submit_for_review(course_id)
        return {"message": "Course submitted for review successfully", "course": updated_course}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{course_id}/approve")
async def approve_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Approve a course (Admin only)
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can approve courses"
        )
    
    course_service = CourseService(db)
    
    try:
        updated_course = course_service.approve_course(course_id)
        return {"message": "Course approved successfully", "course": updated_course}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{course_id}/reject")
async def reject_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reject a course (Admin only)
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can reject courses"
        )
    
    course_service = CourseService(db)
    
    try:
        updated_course = course_service.reject_course(course_id)
        return {"message": "Course rejected successfully", "course": updated_course}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{course_id}/statistics", response_model=CourseStatisticsResponse)
async def get_course_statistics(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get course statistics (Course owner or Admin)
    """
    course_service = CourseService(db)
    
    # Check permissions
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == UserRole.INSTRUCTOR:
        if course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view statistics for your own courses"
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can view course statistics"
        )
    
    try:
        statistics = course_service.get_course_statistics(course_id)
        return statistics
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{course_id}/fee")
async def get_course_fee(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current fee information for a course (including active discounts)
    """
    course_service = CourseService(db)
    
    try:
        fee_info = course_service.get_current_fee(course_id)
        return fee_info
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/status/summary")
async def get_course_status_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get summary of course statuses (Admin or Instructor for their own courses)
    """
    course_service = CourseService(db)
    
    instructor_id = None
    if current_user.role == UserRole.INSTRUCTOR:
        instructor_id = current_user.id
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and instructors can view course status summary"
        )
    
    try:
        summary = course_service.get_course_status_summary(instructor_id)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

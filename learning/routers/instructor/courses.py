from fastapi import APIRouter, HTTPException, status, Depends, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database.db import get_session
from database.models import Course, Instructor
from models.course import CourseCreate, CourseUpdate, Course as CoursePydantic
from middleware.auth import get_current_instructor
from config.logging_config import (
    log_course_operation, log_error, log_db_operation, log_performance,
    log_security_event
)
from exceptions.custom_exceptions import (
    CourseNotFoundException, CourseAccessDeniedException, ValidationException,
    DatabaseException, AuthorizationException
)
from utils.error_utils import (
    validate_course_data, sanitize_input, validate_uuid
)
from services.file_service import file_service
import uuid
import time
from typing import List

router = APIRouter()

@router.post("/create", response_model=CoursePydantic, status_code=status.HTTP_201_CREATED)
async def create_course(
    title: str = Form(...),
    description: str = Form(...),
    banner_image: UploadFile = File(...),
    current_instructor: Instructor = Depends(get_current_instructor),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new course with banner image. Only instructors can create courses.
    """
    start_time = time.time()
    
    try:
        # Validate course data
        validation_result = validate_course_data(title, description)
        if not validation_result["is_valid"]:
            raise ValidationException(
                "Course data validation failed",
                "course_data",
                {"title": title, "description": description}
            )
        
        # Sanitize inputs
        sanitized_title = sanitize_input(title, 255)
        sanitized_description = sanitize_input(description, 1000)
        
        # Generate a unique course ID
        course_id = str(uuid.uuid4())
        
        # Process and save banner image
        banner_image_path = await file_service.process_and_save_banner_image(banner_image, course_id)
        
        # Create the course
        new_course = Course(
            id=course_id,
            title=sanitized_title,
            description=sanitized_description,
            instructor_id=current_instructor.id,
            banner_image=banner_image_path
        )
        
        session.add(new_course)
        await session.commit()
        await session.refresh(new_course)
        
        duration = time.time() - start_time
        log_performance("course_creation", duration, f"Title: {sanitized_title}")
        
        log_course_operation("CREATE", course_id, str(current_instructor.id), f"Title: {sanitized_title}")
        log_db_operation("CREATE", "courses", course_id, f"Instructor: {current_instructor.id}")
        
        return CoursePydantic.from_orm(new_course)
        
    except ValidationException:
        raise
    except Exception as e:
        duration = time.time() - start_time
        log_error("COURSE_CREATION_FAILED", str(e), str(current_instructor.id), f"Duration: {duration:.3f}s")
        raise DatabaseException("Course creation failed", "CREATE", "courses")

@router.post("/create-without-banner", response_model=CoursePydantic, status_code=status.HTTP_201_CREATED)
async def create_course_without_banner(
    course_data: CourseCreate,
    current_instructor: Instructor = Depends(get_current_instructor),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new course without banner image. Only instructors can create courses.
    """
    start_time = time.time()
    
    try:
        # Validate course data
        validation_result = validate_course_data(course_data.title, course_data.description)
        if not validation_result["is_valid"]:
            raise ValidationException(
                "Course data validation failed",
                "course_data",
                {"title": course_data.title, "description": course_data.description}
            )
        
        # Sanitize inputs
        sanitized_title = sanitize_input(course_data.title, 255)
        sanitized_description = sanitize_input(course_data.description, 1000)
        
        # Generate a unique course ID
        course_id = str(uuid.uuid4())
        
        # Create the course without banner image
        new_course = Course(
            id=course_id,
            title=sanitized_title,
            description=sanitized_description,
            instructor_id=current_instructor.id,
            banner_image=None
        )
        
        session.add(new_course)
        await session.commit()
        await session.refresh(new_course)
        
        duration = time.time() - start_time
        log_performance("course_creation", duration, f"Title: {sanitized_title}")
        
        log_course_operation("CREATE", course_id, str(current_instructor.id), f"Title: {sanitized_title}")
        log_db_operation("CREATE", "courses", course_id, f"Instructor: {current_instructor.id}")
        
        return CoursePydantic.from_orm(new_course)
        
    except ValidationException:
        raise
    except Exception as e:
        duration = time.time() - start_time
        log_error("COURSE_CREATION_FAILED", str(e), str(current_instructor.id), f"Duration: {duration:.3f}s")
        raise DatabaseException("Course creation failed", "CREATE", "courses")

@router.get("/all-courses", response_model=List[CoursePydantic])
async def get_all_courses(
    session: AsyncSession = Depends(get_session)
):
    """
    Get all courses in the system. This endpoint is accessible to instructors to view all available courses.
    """
    start_time = time.time()
    
    try:
        query = select(Course)
        result = await session.execute(query)
        courses = result.scalars().all()
        
        duration = time.time() - start_time
        log_performance("get_all_courses", duration, f"Retrieved {len(courses)} courses")
        
        log_db_operation("READ", "courses", details=f"Retrieved all {len(courses)} courses")
        
        return [CoursePydantic.from_orm(course) for course in courses]
        
    except Exception as e:
        duration = time.time() - start_time
        log_error("GET_ALL_COURSES_FAILED", str(e), details=f"Duration: {duration:.3f}s")
        raise DatabaseException("Failed to retrieve all courses", "READ", "courses")
    
@router.put("/course/{course_id}/banner", response_model=CoursePydantic)
async def update_course_banner(
    course_id: str,
    banner_image: UploadFile = File(...),
    current_instructor: Instructor = Depends(get_current_instructor),
    session: AsyncSession = Depends(get_session)
):
    """
    Update course banner image. Only the instructor who created the course can update it.
    """
    start_time = time.time()
    
    try:
        # Validate course ID format
        if not validate_uuid(course_id):
            raise ValidationException("Invalid course ID format", "course_id", course_id)
        
        # First check if the course exists and belongs to the instructor
        query = select(Course).where(
            Course.id == course_id,
            Course.instructor_id == current_instructor.id
        )
        result = await session.execute(query)
        course = result.scalar_one_or_none()
        
        if not course:
            duration = time.time() - start_time
            log_error("COURSE_BANNER_UPDATE_DENIED", f"Course not found or update denied", str(current_instructor.id), 
                     f"Course ID: {course_id}, Duration: {duration:.3f}s")
            log_security_event("UNAUTHORIZED_COURSE_BANNER_UPDATE", str(current_instructor.id), 
                             details=f"Attempted to update banner for course: {course_id}")
            raise CourseAccessDeniedException(course_id, str(current_instructor.id))
        
        # Delete old banner image if exists
        if course.banner_image:
            await file_service.delete_banner_image(course.banner_image)
        
        # Process and save new banner image
        new_banner_path = await file_service.process_and_save_banner_image(banner_image, course_id)
        
        # Update course with new banner image
        course.banner_image = new_banner_path
        await session.commit()
        await session.refresh(course)
        
        duration = time.time() - start_time
        log_performance("course_banner_update", duration, f"Course ID: {course_id}")
        
        log_course_operation("UPDATE_BANNER", course_id, str(current_instructor.id), f"New banner: {new_banner_path}")
        log_db_operation("UPDATE", "courses", course_id, "Updated banner image")
        
        return CoursePydantic.from_orm(course)
        
    except (CourseAccessDeniedException, ValidationException):
        raise
    except Exception as e:
        duration = time.time() - start_time
        log_error("COURSE_BANNER_UPDATE_FAILED", str(e), str(current_instructor.id), 
                 f"Course ID: {course_id}, Duration: {duration:.3f}s")
        raise DatabaseException("Failed to update course banner", "UPDATE", "courses")

@router.get("/my-courses", response_model=List[CoursePydantic])
async def get_my_courses(
    current_instructor: Instructor = Depends(get_current_instructor),
    session: AsyncSession = Depends(get_session)
):
    """
    Get all courses created by the current instructor.
    """
    start_time = time.time()
    
    try:
        query = select(Course).where(Course.instructor_id == current_instructor.id)
        result = await session.execute(query)
        courses = result.scalars().all()
        
        duration = time.time() - start_time
        log_performance("get_my_courses", duration, f"Retrieved {len(courses)} courses")
        
        log_course_operation("READ_ALL", "multiple", str(current_instructor.id), f"Count: {len(courses)}")
        
        return [CoursePydantic.from_orm(course) for course in courses]
        
    except Exception as e:
        duration = time.time() - start_time
        log_error("GET_MY_COURSES_FAILED", str(e), str(current_instructor.id), f"Duration: {duration:.3f}s")
        raise DatabaseException("Failed to retrieve instructor courses", "READ", "courses")

@router.get("/course/{course_id}", response_model=CoursePydantic)
async def get_course(
    course_id: str,
    current_instructor: Instructor = Depends(get_current_instructor),
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific course by ID. Only the instructor who created the course can access it.
    """
    start_time = time.time()
    
    try:
        # Validate course ID format
        if not validate_uuid(course_id):
            raise ValidationException("Invalid course ID format", "course_id", course_id)
        
        query = select(Course).where(
            Course.id == course_id,
            Course.instructor_id == current_instructor.id
        )
        result = await session.execute(query)
        course = result.scalar_one_or_none()
        
        if not course:
            duration = time.time() - start_time
            log_error("COURSE_ACCESS_DENIED", f"Course not found or access denied", str(current_instructor.id), 
                     f"Course ID: {course_id}, Duration: {duration:.3f}s")
            log_security_event("UNAUTHORIZED_COURSE_ACCESS", str(current_instructor.id), 
                             details=f"Attempted to access course: {course_id}")
            raise CourseAccessDeniedException(course_id, str(current_instructor.id))
        
        duration = time.time() - start_time
        log_performance("get_specific_course", duration, f"Course ID: {course_id}")
        
        log_course_operation("READ", course_id, str(current_instructor.id), f"Title: {course.title}")
        
        return CoursePydantic.from_orm(course)
        
    except (CourseAccessDeniedException, ValidationException):
        raise
    except Exception as e:
        duration = time.time() - start_time
        log_error("GET_COURSE_FAILED", str(e), str(current_instructor.id), 
                 f"Course ID: {course_id}, Duration: {duration:.3f}s")
        raise DatabaseException("Failed to retrieve course", "READ", "courses")

@router.put("/course/{course_id}", response_model=CoursePydantic)
async def update_course(
    course_id: str,
    course_data: CourseUpdate,
    current_instructor: Instructor = Depends(get_current_instructor),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a course. Only the instructor who created the course can update it.
    """
    start_time = time.time()
    
    try:
        # Validate course ID format
        if not validate_uuid(course_id):
            raise ValidationException("Invalid course ID format", "course_id", course_id)
        
        # Validate update data if provided
        if course_data.title is not None:
            title_validation = validate_course_data(course_data.title, "dummy")  # We only validate title here
            if not title_validation["is_valid"]:
                raise ValidationException("Invalid course title", "title", course_data.title)
        
        if course_data.description is not None:
            desc_validation = validate_course_data("dummy", course_data.description)  # We only validate description here
            if not desc_validation["is_valid"]:
                raise ValidationException("Invalid course description", "description", course_data.description)
        
        # First check if the course exists and belongs to the instructor
        query = select(Course).where(
            Course.id == course_id,
            Course.instructor_id == current_instructor.id
        )
        result = await session.execute(query)
        course = result.scalar_one_or_none()
        
        if not course:
            duration = time.time() - start_time
            log_error("COURSE_UPDATE_DENIED", f"Course not found or update denied", str(current_instructor.id), 
                     f"Course ID: {course_id}, Duration: {duration:.3f}s")
            log_security_event("UNAUTHORIZED_COURSE_UPDATE", str(current_instructor.id), 
                             details=f"Attempted to update course: {course_id}")
            raise CourseAccessDeniedException(course_id, str(current_instructor.id))
        
        # Sanitize and update the course
        update_data = {}
        if course_data.title is not None:
            sanitized_title = sanitize_input(course_data.title, 255)
            update_data["title"] = sanitized_title
        if course_data.description is not None:
            sanitized_description = sanitize_input(course_data.description, 1000)
            update_data["description"] = sanitized_description
        
        if update_data:
            stmt = update(Course).where(Course.id == course_id).values(**update_data)
            await session.execute(stmt)
            await session.commit()
            await session.refresh(course)
            
            log_db_operation("UPDATE", "courses", course_id, f"Fields updated: {list(update_data.keys())}")
        
        duration = time.time() - start_time
        log_performance("course_update", duration, f"Course ID: {course_id}")
        
        log_course_operation("UPDATE", course_id, str(current_instructor.id), 
                           f"Updated fields: {list(update_data.keys()) if update_data else 'none'}")
        
        return CoursePydantic.from_orm(course)
        
    except (CourseAccessDeniedException, ValidationException):
        raise
    except Exception as e:
        duration = time.time() - start_time
        log_error("COURSE_UPDATE_FAILED", str(e), str(current_instructor.id), 
                 f"Course ID: {course_id}, Duration: {duration:.3f}s")
        raise DatabaseException("Failed to update course", "UPDATE", "courses")

@router.delete("/course/{course_id}")
async def delete_course(
    course_id: str,
    current_instructor: Instructor = Depends(get_current_instructor),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a course. Only the instructor who created the course can delete it.
    """
    start_time = time.time()
    
    try:
        # Validate course ID format
        if not validate_uuid(course_id):
            raise ValidationException("Invalid course ID format", "course_id", course_id)
        
        # First check if the course exists and belongs to the instructor
        query = select(Course).where(
            Course.id == course_id,
            Course.instructor_id == current_instructor.id
        )
        result = await session.execute(query)
        course = result.scalar_one_or_none()
        
        if not course:
            duration = time.time() - start_time
            log_error("COURSE_DELETE_DENIED", f"Course not found or delete denied", str(current_instructor.id), 
                     f"Course ID: {course_id}, Duration: {duration:.3f}s")
            log_security_event("UNAUTHORIZED_COURSE_DELETE", str(current_instructor.id), 
                             details=f"Attempted to delete course: {course_id}")
            raise CourseAccessDeniedException(course_id, str(current_instructor.id))
        
        course_title = course.title  # Store title for logging before deletion
        banner_image_path = course.banner_image  # Store banner path for deletion
        
        # Delete banner image if exists
        if banner_image_path:
            await file_service.delete_banner_image(banner_image_path)
        
        # Delete the course
        await session.delete(course)
        await session.commit()
        
        duration = time.time() - start_time
        log_performance("course_deletion", duration, f"Course ID: {course_id}")
        
        log_course_operation("DELETE", course_id, str(current_instructor.id), f"Title: {course_title}")
        log_db_operation("DELETE", "courses", course_id)
        
        return {"message": "Course deleted successfully"}
        
    except (CourseAccessDeniedException, ValidationException):
        raise
    except Exception as e:
        duration = time.time() - start_time
        log_error("COURSE_DELETE_FAILED", str(e), str(current_instructor.id), 
                 f"Course ID: {course_id}, Duration: {duration:.3f}s")
        raise DatabaseException("Failed to delete course", "DELETE", "courses")


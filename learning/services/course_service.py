from sqlalchemy.orm import Session
from database.models import Course, Enrollment, User
from utils.enums import CourseStatus, UserRole
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy import func

class CourseService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_course(self, course_data: Dict) -> Course:
        """
        Create a new course
        """
        course = Course(**course_data)
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def update_course(self, course_id: str, course_data: Dict) -> Course:
        """
        Update an existing course
        """
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise ValueError("Course not found")
        
        for key, value in course_data.items():
            setattr(course, key, value)
        
        course.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """
        Get course by ID
        """
        return self.db.query(Course).filter(
            Course.id == course_id,
            Course.is_active == True
        ).first()
    
    def get_courses_by_instructor(self, instructor_id: int) -> List[Course]:
        """
        Get all courses by instructor
        """
        return self.db.query(Course).filter(
            Course.instructor_id == instructor_id,
            Course.is_active == True
        ).all()
    
    def get_published_courses(self) -> List[Course]:
        """
        Get all published courses
        """
        return self.db.query(Course).filter(
            Course.status == CourseStatus.PUBLISHED,
            Course.is_active == True
        ).all()
    
    def get_courses_by_status(self, status: CourseStatus) -> List[Course]:
        """
        Get courses by specific status
        """
        return self.db.query(Course).filter(
            Course.status == status,
            Course.is_active == True
        ).all()
    
    def get_enrollable_courses(self) -> List[Course]:
        """
        Get all courses that students can enroll in
        """
        enrollable_statuses = CourseStatus.get_enrollable_statuses()
        return self.db.query(Course).filter(
            Course.status.in_(enrollable_statuses),
            Course.is_active == True
        ).all()
    
    def update_enrollment_count(self, course_id: str) -> int:
        """
        Update and return the total enrollment count for a course
        """
        # Count active enrollments
        enrollment_count = self.db.query(func.count(Enrollment.id)).filter(
            Enrollment.course_id == course_id,
            Enrollment.is_active == True
        ).scalar()
        
        # Update the course's total_enrolled field
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if course:
            course.total_enrolled = enrollment_count
            course.updated_at = datetime.utcnow()
            self.db.commit()
        
        return enrollment_count
    
    def get_current_fee(self, course_id: str) -> Dict:
        """
        Get the current fee for a course (considering discounts)
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        current_time = datetime.utcnow()
        current_fee = course.fee
        is_discounted = False
        
        # Check if discount is active
        if (course.discounted_fee is not None and 
            course.discount_start_date and 
            course.discount_end_date and
            course.discount_start_date <= current_time <= course.discount_end_date):
            current_fee = course.discounted_fee
            is_discounted = True
        
        return {
            "original_fee": course.fee,
            "current_fee": current_fee,
            "discounted_fee": course.discounted_fee,
            "is_discounted": is_discounted,
            "discount_start_date": course.discount_start_date,
            "discount_end_date": course.discount_end_date,
            "discount_percentage": self._calculate_discount_percentage(course.fee, course.discounted_fee) if is_discounted else 0
        }
    
    def _calculate_discount_percentage(self, original_fee: int, discounted_fee: int) -> float:
        """
        Calculate discount percentage
        """
        if original_fee == 0:
            return 0
        return round(((original_fee - discounted_fee) / original_fee) * 100, 2)
    
    def set_course_discount(self, course_id: str, discounted_fee: int, 
                           start_date: datetime, end_date: datetime) -> Course:
        """
        Set discount for a course
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        if discounted_fee >= course.fee:
            raise ValueError("Discounted fee must be less than original fee")
        
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")
        
        course.discounted_fee = discounted_fee
        course.discount_start_date = start_date
        course.discount_end_date = end_date
        course.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def remove_course_discount(self, course_id: str) -> Course:
        """
        Remove discount from a course
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        course.discounted_fee = None
        course.discount_start_date = None
        course.discount_end_date = None
        course.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def publish_course(self, course_id: str) -> Course:
        """
        Publish a course (change status to published)
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        course.status = CourseStatus.PUBLISHED
        course.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def archive_course(self, course_id: str) -> Course:
        """
        Archive a course (change status to archived)
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        course.status = CourseStatus.ARCHIVED
        course.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def suspend_course(self, course_id: str) -> Course:
        """
        Suspend a course (change status to suspended)
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        course.status = CourseStatus.SUSPENDED
        course.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def submit_for_review(self, course_id: str) -> Course:
        """
        Submit a course for review (change status to in_review)
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        course.status = CourseStatus.IN_REVIEW
        course.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def approve_course(self, course_id: str) -> Course:
        """
        Approve a course (change status to approved)
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        course.status = CourseStatus.APPROVED
        course.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def reject_course(self, course_id: str) -> Course:
        """
        Reject a course (change status to rejected)
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        course.status = CourseStatus.REJECTED
        course.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def get_course_statistics(self, course_id: str) -> Dict:
        """
        Get comprehensive statistics for a course
        """
        course = self.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        
        # Get enrollment statistics
        total_enrollments = course.total_enrolled
        
        # Get current fee information
        fee_info = self.get_current_fee(course_id)
        
        # Get recent enrollments (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_enrollments = self.db.query(func.count(Enrollment.id)).filter(
            Enrollment.course_id == course_id,
            Enrollment.enrolled_at >= thirty_days_ago,
            Enrollment.is_active == True
        ).scalar()
        
        return {
            "course_id": course_id,
            "title": course.title,
            "status": course.status.value,
            "status_description": CourseStatus.get_status_description(course.status.value),
            "total_enrollments": total_enrollments,
            "recent_enrollments_30_days": recent_enrollments,
            "fee_information": fee_info,
            "created_at": course.created_at,
            "updated_at": course.updated_at
        }
    
    def search_courses(self, query: str = None, status: CourseStatus = None, 
                      min_fee: int = None, max_fee: int = None) -> List[Course]:
        """
        Search courses with filters
        """
        courses_query = self.db.query(Course).filter(Course.is_active == True)
        
        if query:
            courses_query = courses_query.filter(
                Course.title.ilike(f"%{query}%") | 
                Course.description.ilike(f"%{query}%")
            )
        
        if status:
            courses_query = courses_query.filter(Course.status == status)
        
        if min_fee is not None:
            courses_query = courses_query.filter(Course.fee >= min_fee)
        
        if max_fee is not None:
            courses_query = courses_query.filter(Course.fee <= max_fee)
        
        return courses_query.all()
    
    def get_courses_needing_review(self) -> List[Course]:
        """
        Get all courses that need admin review
        """
        return self.db.query(Course).filter(
            Course.status == CourseStatus.IN_REVIEW,
            Course.is_active == True
        ).all()
    
    def get_course_status_summary(self, instructor_id: int = None) -> Dict:
        """
        Get summary of course statuses
        """
        query = self.db.query(Course.status, func.count(Course.id)).filter(
            Course.is_active == True
        )
        
        if instructor_id:
            query = query.filter(Course.instructor_id == instructor_id)
        
        status_counts = query.group_by(Course.status).all()
        
        summary = {}
        for status, count in status_counts:
            summary[status.value] = {
                "count": count,
                "description": CourseStatus.get_status_description(status.value)
            }
        
        return summary 
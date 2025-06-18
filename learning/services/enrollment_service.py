from sqlalchemy.orm import Session
from database.models import Enrollment, Course, User
from utils.enums import UserRole, CourseStatus
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy import func

class EnrollmentService:
    def __init__(self, db: Session):
        self.db = db
    
    def enroll_student(self, student_id: int, course_id: str) -> Enrollment:
        """
        Enroll a student in a course
        """
        # Check if student exists and is a student
        student = self.db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.STUDENT,
            User.is_active == True
        ).first()
        
        if not student:
            raise ValueError("Student not found or invalid")
        
        # Check if course exists and is enrollable
        course = self.db.query(Course).filter(
            Course.id == course_id,
            Course.is_active == True
        ).first()
        
        if not course:
            raise ValueError("Course not found")
        
        # Check if course status allows enrollment
        enrollable_statuses = CourseStatus.get_enrollable_statuses()
        if course.status not in enrollable_statuses:
            raise ValueError(f"Cannot enroll in course with status: {course.status.value}")
        
        # Check if already enrolled
        existing_enrollment = self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id,
            Enrollment.is_active == True
        ).first()
        
        if existing_enrollment:
            raise ValueError("Student is already enrolled in this course")
        
        # Create enrollment
        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id
        )
        
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        
        # Update course enrollment count
        self._update_course_enrollment_count(course_id)
        
        return enrollment
    
    def unenroll_student(self, student_id: int, course_id: str) -> bool:
        """
        Unenroll a student from a course
        """
        enrollment = self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id,
            Enrollment.is_active == True
        ).first()
        
        if not enrollment:
            raise ValueError("Enrollment not found")
        
        enrollment.is_active = False
        self.db.commit()
        
        # Update course enrollment count
        self._update_course_enrollment_count(course_id)
        
        return True
    
    def get_student_enrollments(self, student_id: int) -> List[Enrollment]:
        """
        Get all enrollments for a student
        """
        return self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.is_active == True
        ).all()
    
    def get_course_enrollments(self, course_id: str) -> List[Enrollment]:
        """
        Get all enrollments for a course
        """
        return self.db.query(Enrollment).filter(
            Enrollment.course_id == course_id,
            Enrollment.is_active == True
        ).all()
    
    def get_enrollment_by_id(self, enrollment_id: int) -> Optional[Enrollment]:
        """
        Get enrollment by ID
        """
        return self.db.query(Enrollment).filter(
            Enrollment.id == enrollment_id,
            Enrollment.is_active == True
        ).first()
    
    def is_student_enrolled(self, student_id: int, course_id: str) -> bool:
        """
        Check if a student is enrolled in a course
        """
        enrollment = self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id,
            Enrollment.is_active == True
        ).first()
        
        return enrollment is not None
    
    def get_enrollment_count(self, course_id: str) -> int:
        """
        Get the number of active enrollments for a course
        """
        return self.db.query(func.count(Enrollment.id)).filter(
            Enrollment.course_id == course_id,
            Enrollment.is_active == True
        ).scalar()
    
    def get_student_courses(self, student_id: int) -> List[Course]:
        """
        Get all courses a student is enrolled in
        """
        enrollments = self.get_student_enrollments(student_id)
        course_ids = [enrollment.course_id for enrollment in enrollments]
        
        return self.db.query(Course).filter(
            Course.id.in_(course_ids),
            Course.is_active == True
        ).all()
    
    def get_instructor_students(self, instructor_id: int) -> List[User]:
        """
        Get all students enrolled in courses by a specific instructor
        """
        # Get all courses by the instructor
        instructor_courses = self.db.query(Course).filter(
            Course.instructor_id == instructor_id,
            Course.is_active == True
        ).all()
        
        course_ids = [course.id for course in instructor_courses]
        
        # Get all enrollments for these courses
        enrollments = self.db.query(Enrollment).filter(
            Enrollment.course_id.in_(course_ids),
            Enrollment.is_active == True
        ).all()
        
        student_ids = list(set([enrollment.student_id for enrollment in enrollments]))
        
        # Get student details
        return self.db.query(User).filter(
            User.id.in_(student_ids),
            User.role == UserRole.STUDENT,
            User.is_active == True
        ).all()
    
    def get_enrollment_statistics(self, course_id: str = None, instructor_id: int = None) -> Dict:
        """
        Get enrollment statistics
        """
        query = self.db.query(Enrollment).filter(Enrollment.is_active == True)
        
        if course_id:
            query = query.filter(Enrollment.course_id == course_id)
        
        if instructor_id:
            # Get courses by instructor
            instructor_courses = self.db.query(Course).filter(
                Course.instructor_id == instructor_id,
                Course.is_active == True
            ).all()
            course_ids = [course.id for course in instructor_courses]
            query = query.filter(Enrollment.course_id.in_(course_ids))
        
        total_enrollments = query.count()
        
        # Get recent enrollments (last 30 days)
        thirty_days_ago = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30)
        recent_enrollments = query.filter(Enrollment.enrolled_at >= thirty_days_ago).count()
        
        # Get enrollments by day (last 7 days)
        daily_enrollments = []
        for i in range(7):
            day_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            
            count = query.filter(
                Enrollment.enrolled_at >= day_start,
                Enrollment.enrolled_at < day_end
            ).count()
            
            daily_enrollments.append({
                "date": day_start.strftime("%Y-%m-%d"),
                "count": count
            })
        
        daily_enrollments.reverse()  # Most recent first
        
        return {
            "total_enrollments": total_enrollments,
            "recent_enrollments_30_days": recent_enrollments,
            "daily_enrollments_last_7_days": daily_enrollments
        }
    
    def _update_course_enrollment_count(self, course_id: str):
        """
        Update the total_enrolled count for a course
        """
        enrollment_count = self.get_enrollment_count(course_id)
        
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if course:
            course.total_enrolled = enrollment_count
            course.updated_at = datetime.utcnow()
            self.db.commit()
    
    def bulk_enroll_students(self, student_ids: List[int], course_id: str) -> List[Enrollment]:
        """
        Enroll multiple students in a course
        """
        enrollments = []
        
        for student_id in student_ids:
            try:
                enrollment = self.enroll_student(student_id, course_id)
                enrollments.append(enrollment)
            except ValueError as e:
                # Log error but continue with other enrollments
                print(f"Failed to enroll student {student_id}: {str(e)}")
                continue
        
        return enrollments
    
    def get_enrollment_history(self, student_id: int = None, course_id: str = None) -> List[Enrollment]:
        """
        Get enrollment history (including inactive enrollments)
        """
        query = self.db.query(Enrollment)
        
        if student_id:
            query = query.filter(Enrollment.student_id == student_id)
        
        if course_id:
            query = query.filter(Enrollment.course_id == course_id)
        
        return query.order_by(Enrollment.enrolled_at.desc()).all() 
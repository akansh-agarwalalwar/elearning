from enum import Enum
from typing import List

class PrivilegeName(Enum):
    """
    Enum for privilege names that can be assigned to instructors
    """
    # Course Management Privileges
    CREATE_COURSE = "create_course"
    EDIT_COURSE = "edit_course"
    DELETE_COURSE = "delete_course"
    PUBLISH_COURSE = "publish_course"
    ARCHIVE_COURSE = "archive_course"
    SUSPEND_COURSE = "suspend_course"
    
    # Lesson Management Privileges
    CREATE_LESSON = "create_lesson"
    EDIT_LESSON = "edit_lesson"
    DELETE_LESSON = "delete_lesson"
    MANAGE_LESSONS = "manage_lessons"
    
    # Assignment Management Privileges
    CREATE_ASSIGNMENT = "create_assignment"
    EDIT_ASSIGNMENT = "edit_assignment"
    DELETE_ASSIGNMENT = "delete_assignment"
    MANAGE_ASSIGNMENTS = "manage_assignments"
    GRADE_ASSIGNMENTS = "grade_assignments"
    
    # Student Management Privileges
    VIEW_ENROLLMENTS = "view_enrollments"
    MANAGE_STUDENTS = "manage_students"
    ENROLL_STUDENTS = "enroll_students"
    UNENROLL_STUDENTS = "unenroll_students"
    
    # Course Content Privileges
    UPLOAD_CONTENT = "upload_content"
    DELETE_CONTENT = "delete_content"
    MANAGE_CONTENT = "manage_content"
    
    # Analytics and Reporting Privileges
    VIEW_ANALYTICS = "view_analytics"
    VIEW_REPORTS = "view_reports"
    EXPORT_DATA = "export_data"
    
    # Communication Privileges
    SEND_ANNOUNCEMENTS = "send_announcements"
    MESSAGE_STUDENTS = "message_students"
    MANAGE_COMMUNICATIONS = "manage_communications"
    
    # Financial Privileges
    SET_DISCOUNTS = "set_discounts"
    VIEW_REVENUE = "view_revenue"
    MANAGE_PRICING = "manage_pricing"
    
    # System Privileges
    MANAGE_COURSE_SETTINGS = "manage_course_settings"
    ACCESS_ADVANCED_FEATURES = "access_advanced_features"
    
    @classmethod
    def get_default_instructor_privileges(cls) -> List[str]:
        """
        Get the default privileges assigned to new instructors
        """
        return [
            cls.CREATE_COURSE.value,
            cls.EDIT_COURSE.value,
            cls.DELETE_COURSE.value,
            cls.MANAGE_LESSONS.value,
            cls.VIEW_ENROLLMENTS.value,
            cls.CREATE_ASSIGNMENT.value,
            cls.GRADE_ASSIGNMENTS.value,
            cls.UPLOAD_CONTENT.value,
            cls.SEND_ANNOUNCEMENTS.value,
            cls.SET_DISCOUNTS.value
        ]
    
    @classmethod
    def get_privilege_description(cls, privilege_name: str) -> str:
        """
        Get the description for a privilege
        """
        descriptions = {
            cls.CREATE_COURSE.value: "Can create new courses",
            cls.EDIT_COURSE.value: "Can edit course details and settings",
            cls.DELETE_COURSE.value: "Can delete courses",
            cls.PUBLISH_COURSE.value: "Can publish courses for student enrollment",
            cls.ARCHIVE_COURSE.value: "Can archive completed or outdated courses",
            cls.SUSPEND_COURSE.value: "Can temporarily suspend course access",
            cls.CREATE_LESSON.value: "Can create new lessons within courses",
            cls.EDIT_LESSON.value: "Can edit lesson content and settings",
            cls.DELETE_LESSON.value: "Can delete lessons",
            cls.MANAGE_LESSONS.value: "Can manage all aspects of lessons",
            cls.CREATE_ASSIGNMENT.value: "Can create new assignments",
            cls.EDIT_ASSIGNMENT.value: "Can edit assignment details",
            cls.DELETE_ASSIGNMENT.value: "Can delete assignments",
            cls.MANAGE_ASSIGNMENTS.value: "Can manage all aspects of assignments",
            cls.GRADE_ASSIGNMENTS.value: "Can grade student assignments",
            cls.VIEW_ENROLLMENTS.value: "Can view student enrollments",
            cls.MANAGE_STUDENTS.value: "Can manage student access and permissions",
            cls.ENROLL_STUDENTS.value: "Can manually enroll students in courses",
            cls.UNENROLL_STUDENTS.value: "Can remove students from courses",
            cls.UPLOAD_CONTENT.value: "Can upload course materials and resources",
            cls.DELETE_CONTENT.value: "Can delete uploaded content",
            cls.MANAGE_CONTENT.value: "Can manage all course content",
            cls.VIEW_ANALYTICS.value: "Can view course analytics and insights",
            cls.VIEW_REPORTS.value: "Can view detailed course reports",
            cls.EXPORT_DATA.value: "Can export course data and reports",
            cls.SEND_ANNOUNCEMENTS.value: "Can send announcements to enrolled students",
            cls.MESSAGE_STUDENTS.value: "Can send direct messages to students",
            cls.MANAGE_COMMUNICATIONS.value: "Can manage all communication features",
            cls.SET_DISCOUNTS.value: "Can set course discounts and pricing",
            cls.VIEW_REVENUE.value: "Can view course revenue and financial data",
            cls.MANAGE_PRICING.value: "Can manage course pricing and payment settings",
            cls.MANAGE_COURSE_SETTINGS.value: "Can access advanced course settings",
            cls.ACCESS_ADVANCED_FEATURES.value: "Can access advanced platform features"
        }
        return descriptions.get(privilege_name, "No description available")

class CourseStatus(Enum):
    """
    Enum for course status values
    """
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    
    @classmethod
    def get_active_statuses(cls) -> List[str]:
        """
        Get statuses that indicate an active course
        """
        return [cls.PUBLISHED.value, cls.APPROVED.value]
    
    @classmethod
    def get_inactive_statuses(cls) -> List[str]:
        """
        Get statuses that indicate an inactive course
        """
        return [cls.DRAFT.value, cls.ARCHIVED.value, cls.SUSPENDED.value, cls.IN_REVIEW.value, cls.REJECTED.value]
    
    @classmethod
    def get_enrollable_statuses(cls) -> List[str]:
        """
        Get statuses that allow student enrollment
        """
        return [cls.PUBLISHED.value, cls.APPROVED.value]
    
    @classmethod
    def get_status_description(cls, status: str) -> str:
        """
        Get the description for a course status
        """
        descriptions = {
            cls.DRAFT.value: "Course is in draft mode and not visible to students",
            cls.PUBLISHED.value: "Course is published and available for enrollment",
            cls.ARCHIVED.value: "Course is archived and no longer available",
            cls.SUSPENDED.value: "Course is temporarily suspended",
            cls.IN_REVIEW.value: "Course is under review by administrators",
            cls.APPROVED.value: "Course has been approved and is available",
            cls.REJECTED.value: "Course has been rejected and needs revision"
        }
        return descriptions.get(status, "Unknown status")

class UserRole(Enum):
    """
    Enum for user roles
    """
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"
    
    @classmethod
    def get_all_roles(cls) -> List[str]:
        """
        Get all available user roles
        """
        return [role.value for role in cls]
    
    @classmethod
    def get_staff_roles(cls) -> List[str]:
        """
        Get roles that have administrative or teaching capabilities
        """
        return [cls.ADMIN.value, cls.INSTRUCTOR.value]
    
    @classmethod
    def get_role_description(cls, role: str) -> str:
        """
        Get the description for a user role
        """
        descriptions = {
            cls.ADMIN.value: "System administrator with full access",
            cls.INSTRUCTOR.value: "Course instructor with teaching capabilities",
            cls.STUDENT.value: "Student with learning access"
        }
        return descriptions.get(role, "Unknown role")

class AssignmentStatus(Enum):
    """
    Enum for assignment status values
    """
    DRAFT = "draft"
    PUBLISHED = "published"
    SUBMITTED = "submitted"
    GRADED = "graded"
    LATE = "late"
    OVERDUE = "overdue"
    
    @classmethod
    def get_active_statuses(cls) -> List[str]:
        """
        Get statuses that indicate an active assignment
        """
        return [cls.PUBLISHED.value, cls.SUBMITTED.value, cls.GRADED.value]
    
    @classmethod
    def get_status_description(cls, status: str) -> str:
        """
        Get the description for an assignment status
        """
        descriptions = {
            cls.DRAFT.value: "Assignment is in draft mode",
            cls.PUBLISHED.value: "Assignment is published and available to students",
            cls.SUBMITTED.value: "Assignment has been submitted by student",
            cls.GRADED.value: "Assignment has been graded by instructor",
            cls.LATE.value: "Assignment was submitted after the due date",
            cls.OVERDUE.value: "Assignment is past the due date and not submitted"
        }
        return descriptions.get(status, "Unknown status") 
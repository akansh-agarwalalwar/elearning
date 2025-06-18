from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    # role = Column(SQLEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    courses = relationship("Course", back_populates="instructor")
    enrollments = relationship("Enrollment", back_populates="student")
    assigned_privileges = relationship("Privilege", back_populates="instructor")

class Privilege(Base):
    __tablename__ = "privileges"
    
    id = Column(Integer, primary_key=True)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    privilege_name = Column(String(100), nullable=False)  # Uses values from PrivilegeName enum
    privilege_description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Admin who assigned the privilege
    assigned_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    instructor = relationship("User", foreign_keys=[instructor_id], back_populates="assigned_privileges")
    admin = relationship("User", foreign_keys=[assigned_by])

class Course(Base):
    __tablename__ = "courses"

    id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    banner_image = Column(String(500), nullable=True)  # Path to banner image
    fee = Column(Integer, nullable=False, default=0)  # Course fee in cents/smallest currency unit
    discounted_fee = Column(Integer, nullable=True)  # Discounted fee in cents/smallest currency unit
    discount_start_date = Column(DateTime, nullable=True)  # When discount starts
    discount_end_date = Column(DateTime, nullable=True)  # When discount ends
    total_enrolled = Column(Integer, default=0, nullable=False)  # Total number of enrolled students
    # status = Column(SQLEnum(CourseStatus), default=CourseStatus.DRAFT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    instructor = relationship("User", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(255), primary_key=True)
    course_id = Column(String(255), ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    course = relationship("Course", back_populates="lessons")
    assignments = relationship("Assignment", back_populates="lesson")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(String(255), ForeignKey("lessons.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    due_date = Column(DateTime, nullable=False)
    # status = Column(SQLEnum(AssignmentStatus), default=AssignmentStatus.DRAFT, nullable=False)
    submitted_at = Column(DateTime, server_default=func.now(), nullable=False)
    score = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    lesson = relationship("Lesson", back_populates="assignments")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(String(255), ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
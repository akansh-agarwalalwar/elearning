from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .db import Base

class BaseUser(Base):
    __tablename__ = "base_user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    user_type = Column(String(20), nullable=False)  # 'admin', 'student', or 'instructor'

class Admin(Base):
    __tablename__ = "admin"
    
    id = Column(Integer, primary_key=True)
    base_user_id = Column(Integer, ForeignKey("base_user.id"), nullable=False)
    
    # Relationships
    base_user = relationship("BaseUser")

class Student(Base):
    __tablename__ = "student"
    
    id = Column(Integer, primary_key=True)
    base_user_id = Column(Integer, ForeignKey("base_user.id"), nullable=False)
    
    # Relationships
    base_user = relationship("BaseUser")
    enrollments = relationship("Enrollment", back_populates="student")

class Instructor(Base):
    __tablename__ = "instructor"
    
    id = Column(Integer, primary_key=True)
    base_user_id = Column(Integer, ForeignKey("base_user.id"), nullable=False)
    
    # Relationships
    base_user = relationship("BaseUser")
    courses = relationship("Course", back_populates="instructor")

class Course(Base):
    __tablename__ = "courses"

    id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructor.id"), nullable=False)

    # Relationships
    instructor = relationship("Instructor", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(255), primary_key=True)
    course_id = Column(String(255), ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="lessons")
    assignments = relationship("Assignment", back_populates="lesson")

class Assignment(Base):
    __tablename__ = "assignment"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(String(255), ForeignKey("lessons.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(String(255), nullable=False)
    submitted_at = Column(DateTime, server_default=func.now(), nullable=False)
    score = Column(Integer, nullable=False)

    # Relationships
    lesson = relationship("Lesson", back_populates="assignments")

class Enrollment(Base):
    __tablename__ = "enrollment"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    course_id = Column(String(255), ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
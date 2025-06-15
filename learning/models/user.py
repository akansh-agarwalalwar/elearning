from pydantic import BaseModel, EmailStr

class BaseUserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    user_type: str = "student"  # Default to 'student' if not provided

class BaseUser(BaseUserIn):
    id: int

    class Config:
        from_attributes = True

class AdminIn(BaseModel):
    base_user_id: int

class Admin(AdminIn):
    id: int

    class Config:
        from_attributes = True

class StudentIn(BaseModel):
    base_user_id: int

class Student(StudentIn):
    id: int

    class Config:
        from_attributes = True

class InstructorIn(BaseModel):
    base_user_id: int

class Instructor(InstructorIn):
    id: int

    class Config:
        from_attributes = True

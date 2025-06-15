from pydantic import BaseModel
from datetime import date

class AssignmentBase(BaseModel):
    title: str
    description: str
    due_date: date
    status: str

class AssignmentCreate(AssignmentBase):
    lesson_id: int

class Assignment(AssignmentBase):
    id: int
    lesson_id: int

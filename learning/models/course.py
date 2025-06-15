from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: str = None

class CourseCreate(CourseBase):
    instructor_id: int

class Course(CourseBase):
    id: int
    instructor_id: int

    class Config:
        orm_mode = True

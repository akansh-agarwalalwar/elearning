from pydantic import BaseModel

class LessonBase(BaseModel):
    title: str
    content: str
    order: int

class LessonCreate(LessonBase):
    course_id: int

class Lesson(LessonBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True

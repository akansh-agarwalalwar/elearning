from pydantic import BaseModel, ConfigDict
from typing import Optional
from fastapi import UploadFile


class CourseBase(BaseModel):
    title: str
    description: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    banner_image: Optional[str] = None

class Course(CourseBase):
    id: str
    instructor_id: int
    banner_image: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class CourseWithFile(BaseModel):
    title: str
    description: str
    banner_image: UploadFile

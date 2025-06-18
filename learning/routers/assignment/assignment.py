from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.connection import get_db
from database.models import Assignment
from models.assignment import AssignmentBase, AssignmentCreate, Assignment as AssignmentPydantic

router = APIRouter()

@router.post("/create-assignment", response_model=AssignmentPydantic)
def create_assignment(assignment: AssignmentBase, session: Session = Depends(get_db)):
    existing = session.query(Assignment).filter(Assignment.id == assignment.id).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Assignment already exists")
    
    new_assignment = Assignment(**assignment.dict())
    session.add(new_assignment)
    session.commit()
    session.refresh(new_assignment)
    
    return AssignmentPydantic.from_orm(new_assignment)

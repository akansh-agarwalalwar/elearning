from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_session
from database.models import Assignment
from models.assignment import AssignmentBase, AssignmentCreate, Assignment as AssignmentPydantic

router = APIRouter()

@router.post("/create-assignment", response_model=AssignmentPydantic)
async def create_assignment(assignment: AssignmentBase, session: AsyncSession = Depends(get_session)):
    query = select(Assignment).where(Assignment.id == assignment.id)
    result = await session.execute(query)
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Assignment already exists")
    
    new_assignment = Assignment(**assignment.dict())
    session.add(new_assignment)
    await session.commit()
    await session.refresh(new_assignment)
    
    return AssignmentPydantic.from_orm(new_assignment)

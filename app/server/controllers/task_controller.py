from services import task_service
from database import get_db
from fastapi import APIRouter, Depends
from schemas.task_schema import TaskSchema, CreateTaskSchema, DeleteTaskSchema
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/", response_model=List[TaskSchema])
async def get_all(db: Session = Depends(get_db)):
    return task_service.get_all(db=db)


@router.post("/", response_model=TaskSchema)
async def create(create_task_schema: CreateTaskSchema, db: Session = Depends(get_db)):
    return task_service.create(
        db=db,
        title=create_task_schema.title,
        description=create_task_schema.description,
    )


@router.delete("/{task_id}", response_model=None)
async def delete(task_id: int, db: Session = Depends(get_db)):
    task_service.delete(db, task_id)

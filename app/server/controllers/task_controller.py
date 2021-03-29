from services import task_service
from database import get_db
from fastapi import APIRouter, Depends
from schemas.task_schema import (
    TaskSchema,
    CreateTaskSchema,
    UpdateTaskStatusSchema,
    UpdateTaskPrioritySchema,
    AssignTaskSchema,
)
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


@router.put("/{task_id}/status", response_model=TaskSchema)
async def update_status(
    task_id: int,
    update_task_status_schema: UpdateTaskStatusSchema,
    db: Session = Depends(get_db),
):
    return task_service.update_status(
        db=db, task_id=task_id, new_status=update_task_status_schema.new_status
    )


@router.put("/{task_id}/priority", response_model=TaskSchema)
async def update_priority(
    task_id: int,
    update_task_priority_schema: UpdateTaskPrioritySchema,
    db: Session = Depends(get_db),
):
    return task_service.update_priority(
        db=db, task_id=task_id, new_priority=update_task_priority_schema.new_priority
    )


@router.post("/assign", response_model=TaskSchema)
async def assign_task(
    assign_task_schema: AssignTaskSchema,
    db: Session = Depends(get_db),
):
    return task_service.assign(
        db, assign_task_schema.task_id, assign_task_schema.user_id
    )


@router.delete("/{task_id}", response_model=None)
async def delete(task_id: int, db: Session = Depends(get_db)):
    task_service.delete(db, task_id)

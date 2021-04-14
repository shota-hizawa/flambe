from services import task_service
from database import get_db
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from schemas.task_schema import (
    TaskSchema,
    CreateTaskSchema,
    UpdateTaskStatusSchema,
    UpdateTaskPrioritySchema,
    AssignTaskSchema,
    RemoveAssignmentTaskSchema,
    GetTasksFilteredByStatusAndPrioritySchema,
)
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("", response_model=Page[TaskSchema])
async def get_all_tasks(db: Session = Depends(get_db)):
    return paginate(task_service.get_all(db=db))


@router.post("/search", response_model=Page[TaskSchema])
async def get_tasks_filtered_by_status_and_priority(
    get_tasks_filtered_by_status_and_priority_schema: GetTasksFilteredByStatusAndPrioritySchema,
    db: Session = Depends(get_db),
):
    return paginate(
        task_service.get_tasks_filtered_by_status_and_priority_schema(
            filtering_statuses=get_tasks_filtered_by_status_and_priority_schema.statuses,
            filtering_priorities=get_tasks_filtered_by_status_and_priority_schema.priorities,
            db=db,
        )
    )


@router.get("/incomplete", response_model=List[TaskSchema])
async def get_incomplete_tasks(db: Session = Depends(get_db)):
    return task_service.get_incomplete_tasks(db=db)


@router.get("/incomplete/not-assigned", response_model=List[TaskSchema])
async def get_incomplete_and_not_assigned_tasks(db: Session = Depends(get_db)):
    return task_service.get_incomplete_and_not_assigned_tasks(db=db)


@router.post("", response_model=TaskSchema)
async def create_task(
    create_task_schema: CreateTaskSchema, db: Session = Depends(get_db)
):
    return task_service.create(
        db=db,
        title=create_task_schema.title,
        description=create_task_schema.description,
        priority=create_task_schema.priority,
    )


@router.put("/{task_id}/status", response_model=TaskSchema)
async def update_task_status(
    task_id: int,
    update_task_status_schema: UpdateTaskStatusSchema,
    db: Session = Depends(get_db),
):
    return task_service.update_status(
        db=db, task_id=task_id, new_status=update_task_status_schema.new_status
    )


@router.put("/{task_id}/priority", response_model=TaskSchema)
async def update_task_priority(
    task_id: int,
    update_task_priority_schema: UpdateTaskPrioritySchema,
    db: Session = Depends(get_db),
):
    return task_service.update_priority(
        db=db, task_id=task_id, new_priority=update_task_priority_schema.new_priority
    )


@router.post("/assign", response_model=TaskSchema)
async def assign_task_to_user(
    assign_task_schema: AssignTaskSchema,
    db: Session = Depends(get_db),
):
    return task_service.assign(
        db, assign_task_schema.task_id, assign_task_schema.user_id
    )


@router.post("/remove-assign", response_model=TaskSchema)
async def remove_assignment_from_user(
    remove_assignment_task_schema: RemoveAssignmentTaskSchema,
    db: Session = Depends(get_db),
):
    return task_service.remove_assignment(
        db, remove_assignment_task_schema.task_id, remove_assignment_task_schema.user_id
    )


@router.delete("/{task_id}", response_model=None)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service.delete(db, task_id)

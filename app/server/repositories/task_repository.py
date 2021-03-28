from entities.task import Task, Status, Priority
from sqlalchemy.orm import Session
from typing import List, Optional
from exceptions import *


def find_all(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.deleted == False).all()  # noqa


def find_by_id(db: Session, task_id: int) -> Task:
    task = db.query(Task).get(task_id)
    if task is None:
        raise ApplicationException(ErrorMessages.TaskIsNotFound)
    return task


def create(db: Session, title: str, description: Optional[str]) -> Task:
    created_task = Task(title=title, description=description)
    db.add(created_task)
    return created_task


def update_status(updated_task: Task, new_status: Status) -> Task:
    updated_task.status = new_status
    return updated_task


def update_priority(updated_task: Task, new_priority: Priority) -> Task:
    updated_task.priority = new_priority
    return updated_task


def soft_delete(deleted_task: Task):
    deleted_task.deleted = True

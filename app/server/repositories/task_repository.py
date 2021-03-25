from entities import Task
from sqlalchemy.orm import Session
from typing import List, Optional


def find_all(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.deleted == False).all()  # noqa


def find_by_id(db: Session, task_id: int) -> Task:
    return db.query(Task).get(task_id)


def create(db: Session, title: str, description: Optional[str]) -> Task:
    created_task = Task(title=title, description=description)
    db.add(created_task)
    return created_task


def soft_delete(deleted_task: Task):
    deleted_task.deleted = True

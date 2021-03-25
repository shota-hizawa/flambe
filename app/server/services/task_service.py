from repositories import task_repository
from sqlalchemy.orm import Session
from utils.crypt import encrypt
from typing import List, Optional, cast
from entities import Task


def get_all(db: Session) -> List[Task]:
    return task_repository.find_all(db=db)


def create(db: Session, title: str, description: Optional[str]) -> Task:
    created_task = task_repository.create(db=db, title=title, description=description)
    db.commit()
    return created_task


def delete(db, task_id: int):
    task = task_repository.find_by_id(db=db, task_id=task_id)
    if task is not None:
        task = cast(Task, task)
        task_repository.soft_delete(task)
    else:
        raise Exception("user not found.")
    db.commit()

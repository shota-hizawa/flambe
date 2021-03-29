from repositories import task_repository
from sqlalchemy.orm import Session
from typing import List, Optional, cast
from entities.task import Task, Status, Priority
from exceptions import *


def get_all(db: Session) -> List[Task]:
    return task_repository.find_all(db=db)


def create(db: Session, title: str, description: Optional[str]) -> Task:
    created_task = task_repository.create(db=db, title=title, description=description)
    db.commit()
    return created_task


def update_status(db: Session, task_id: int, new_status: Status) -> Task:
    updated_task = __get_task_by_id(db=db, task_id=task_id)
    task_repository.update_status(updated_task=updated_task, new_status=new_status)
    db.commit()
    return updated_task


def update_priority(db: Session, task_id: int, new_priority: Priority) -> Task:
    updated_task = __get_task_by_id(db=db, task_id=task_id)
    task_repository.update_priority(
        updated_task=updated_task, new_priority=new_priority
    )
    db.commit()
    return updated_task


def delete(db, task_id: int) -> None:
    deleted_task = __get_task_by_id(db=db, task_id=task_id)
    task_repository.delete(db, deleted_task)
    db.commit()


def __get_task_by_id(db, task_id: int) -> Task:
    task = task_repository.find_by_id(db=db, task_id=task_id)
    if task is not None:
        return cast(Task, task)
    else:
        raise ApplicationException(ErrorMessages.TaskIsNotFound)
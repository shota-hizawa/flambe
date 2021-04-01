from repositories import task_repository
from services import user_service
from sqlalchemy.orm import Session
from typing import List, Optional, cast
from entities.task import Task, Status, Priority
from exceptions import *
from utils.sort import sort_tasks_by_priority


def get_all(db: Session) -> List[Task]:
    return task_repository.find_all(db=db)


def get_incomplete_tasks(db: Session) -> List[Task]:
    tasks = task_repository.find_by_status_not_done(db=db)

    doing_tasks = sort_tasks_by_priority(
        list(filter(lambda task: task.status is Status.DOING, tasks))
    )
    todo_tasks = sort_tasks_by_priority(
        list(filter(lambda task: task.status is Status.TODO, tasks))
    )
    return [*doing_tasks, *todo_tasks]


def get_incomplete_and_not_assigned_tasks(db: Session) -> List[Task]:
    return list(
        filter(
            lambda task: len(task.assignees) is 0,
            sort_tasks_by_priority(task_repository.find_by_status_not_done(db=db)),
        )
    )


def create(
    db: Session,
    title: str,
    description: Optional[str],
    priority: Priority,
) -> Task:
    created_task = task_repository.create(
        db=db, title=title, description=description, priority=priority
    )
    db.commit()
    return created_task


def update_status(db: Session, task_id: int, new_status: Status) -> Task:
    updated_task = get_task_by_id(db=db, task_id=task_id)
    task_repository.update_status(updated_task=updated_task, new_status=new_status)
    db.commit()
    return updated_task


def update_priority(db: Session, task_id: int, new_priority: Priority) -> Task:
    updated_task = get_task_by_id(db=db, task_id=task_id)
    task_repository.update_priority(
        updated_task=updated_task, new_priority=new_priority
    )
    db.commit()
    return updated_task


def assign(db: Session, task_id: int, user_id: int) -> Task:
    task = get_task_by_id(db=db, task_id=task_id)
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    task_repository.assign_user(updated_task=task, new_assignee=user)
    db.commit()
    return task


def remove_assignment(db: Session, task_id: int, user_id: int) -> Task:
    task = get_task_by_id(db=db, task_id=task_id)
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    if user in task.assignees:
        task_repository.remove_assignment_from_user(updated_task=task, assignee=user)
    else:
        raise ApplicationException(ErrorMessages.UserIsNotAssignedToTheTask)
    db.commit()
    return task


def delete(db, task_id: int) -> None:
    deleted_task = get_task_by_id(db=db, task_id=task_id)
    task_repository.delete(db, deleted_task)
    db.commit()


def get_task_by_id(db, task_id: int) -> Task:
    task = task_repository.find_by_id(db=db, task_id=task_id)
    if task is not None:
        return cast(Task, task)
    else:
        raise ApplicationException(ErrorMessages.TaskIsNotFound)

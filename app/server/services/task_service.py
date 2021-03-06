from repositories import task_repository
from services import user_service
from sqlalchemy.orm import Session
from typing import List, Optional, cast, Tuple
from entities.task import Task, Status, Priority, get_incomplete_status
from exceptions import *
from fastapi_pagination import Params


def get_all_by_pagination(db: Session, params: Params) -> Tuple[List[Task], int]:
    return task_repository.find_all_by_pagination(db=db, params=params)


def get_tasks_filtered_by_status_and_priority_by_pagination(
    filtering_statuses: List[Status],
    filtering_priorities: List[Priority],
    db: Session,
    params: Params,
) -> Tuple[List[Task], int]:
    # 指定されてない条件は全検索にする
    if len(filtering_statuses) == 0:
        filtering_statuses = list(map(Status, Status))
    if len(filtering_priorities) == 0:
        filtering_priorities = list(map(Priority, Priority))

    return task_repository.find_by_statuses_and_priorities_by_pagination(
        filtering_statuses=filtering_statuses,
        filtering_priorities=filtering_priorities,
        db=db,
        params=params,
    )


def get_incomplete_tasks(db: Session) -> List[Task]:
    return task_repository.find_by_statuses_order_by_status_and_priority(
        filtering_statuses=get_incomplete_status(), db=db
    )


def get_incomplete_and_not_assigned_tasks(db: Session) -> List[Task]:
    return task_repository.find_by_statuses_and_without_assignees_order_by_status_and_priority(
        filtering_statuses=get_incomplete_status(), db=db
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

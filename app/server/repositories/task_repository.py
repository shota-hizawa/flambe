from entities.task import Task, Status, Priority
from entities.user import User
from entities.task_assignment import TaskAssignment
from sqlalchemy.orm import Session
from sqlalchemy import case, desc, func
from typing import List, Optional, cast
from exceptions import *


def find_all(db: Session) -> List[Task]:
    return db.query(Task).all()  # noqa


def find_by_id(db: Session, task_id: int) -> Task:
    task = db.query(Task).get(task_id)
    if task is None:
        raise ApplicationException(ErrorMessages.TaskIsNotFound)
    task = cast(Task, task)
    return task


def find_by_status_not_done(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.status is not Status.DONE).all()


def find_by_statuses_order_by_status_asc_and_priority_desc(
    filtering_statuses: List[Status], db: Session
) -> List[Task]:
    return (
        db.query(Task)
        .filter(Task.status.in_(filtering_statuses))
        .order_by(status_sort(), desc(priority_sort()))
        .all()
    )


def find_by_user_id_and_status_order_by_status_asc_and_priority_desc(
    user_id: int, filtering_statuses: List[Status], db: Session
) -> List[Task]:
    return (
        db.query(Task)
        .outerjoin(TaskAssignment)
        .filter(Task.status.in_(filtering_statuses), TaskAssignment.user_id == user_id)
        .order_by(status_sort(), desc(priority_sort()))
        .all()
    )


def find_by_statuses_and_without_assignees_order_by_status_asc_and_priority_desc(
    filtering_statuses: List[Status], db: Session
) -> List[Task]:
    # アサイン0のタスクIDを抽出
    task_ids_without_assignees = [
        result.id
        for result in (
            db.query(Task.id)
            .outerjoin(TaskAssignment)
            .having(func.count(TaskAssignment.user_id) == 0)
            .group_by(Task.id)
            .all()
        )
    ]

    return (
        db.query(Task)
        .filter(
            Task.status.in_(filtering_statuses), Task.id.in_(task_ids_without_assignees)
        )
        .order_by(status_sort(), desc(priority_sort()))
        .all()
    )


def find_by_statuses_and_priorities(
    filtering_statuses: List[Status], filtering_priorities: List[Priority], db: Session
) -> List[Task]:
    return (
        db.query(Task)
        .filter(
            Task.status.in_(filtering_statuses), Task.priority.in_(filtering_priorities)
        )
        .all()
    )


def create(
    db: Session,
    title: str,
    description: Optional[str],
    priority: Priority,
) -> Task:
    created_task = Task(title=title, description=description, priority=priority)
    db.add(created_task)
    return created_task


def update_status(updated_task: Task, new_status: Status) -> Task:
    updated_task.status = new_status
    return updated_task


def update_priority(updated_task: Task, new_priority: Priority) -> Task:
    updated_task.priority = new_priority
    return updated_task


def assign_user(updated_task: Task, new_assignee: User) -> Task:
    updated_task.assignees.append(new_assignee)
    return updated_task


def remove_assignment_from_user(updated_task: Task, assignee: User) -> Task:
    updated_task.assignees.remove(assignee)
    return updated_task


def delete(db: Session, deleted_task: Task) -> None:
    db.delete(deleted_task)


def status_sort():
    whens = {Status.TODO: 0, Status.DOING: 1, Status.DONE: 2}
    return case(value=Task.status, whens=whens).label("status")


def priority_sort():
    whens = {Priority.LOW: 0, Priority.MEDIUM: 1, Priority.HIGH: 2}
    return case(value=Task.priority, whens=whens).label("priority")

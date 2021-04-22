from entities.task import Task, Status, Priority
from entities.user import User
from entities.task_assignment import TaskAssignment
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, cast, Tuple
from exceptions import *
from fastapi_pagination import Params


def find_all_by_pagination(db: Session, params: Params) -> Tuple[List[Task], int]:
    return (
        db.query(Task).limit(params.size).offset(params.size * params.page).all(),
        db.query(func.count(Task.id).label("total")).first().total,
    )


def find_by_id(db: Session, task_id: int) -> Task:
    task = db.query(Task).get(task_id)
    if task is None:
        raise ApplicationException(ErrorMessages.TaskIsNotFound)
    task = cast(Task, task)
    return task


def find_by_status_not_done(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.status is not Status.DONE).all()


def find_by_statuses_order_by_status_and_priority(
    filtering_statuses: List[Status], db: Session
) -> List[Task]:
    """
    フィルタ対象のステータスに一致したタスクを取得し、
    ・ステータス（TODO-DOING-DONE）
    ・優先度（HIGH-MEDIUM-LOW）
    で並び替えて返却する。
    """
    return (
        db.query(Task)
        .filter(Task.status.in_(filtering_statuses))
        .order_by(Task.status, Task.priority)
        .all()
    )


def find_by_user_id_and_status_order_by_status_and_priority(
    user_id: int, filtering_statuses: List[Status], db: Session
) -> List[Task]:
    """
    フィルタ対象のステータスに一致しかつ指定されたユーザがアサインされているタスクを取得し、
    ・ステータス（TODO-DOING-DONE）
    ・優先度（HIGH-MEDIUM-LOW）
    で並び替えて返却する。
    """
    return (
        db.query(Task)
        .outerjoin(TaskAssignment)
        .filter(Task.status.in_(filtering_statuses), TaskAssignment.user_id == user_id)
        .order_by(Task.status, Task.priority)
        .all()
    )


def find_by_statuses_and_without_assignees_order_by_status_and_priority(
    filtering_statuses: List[Status], db: Session
) -> List[Task]:
    """
    フィルタ対象のステータスに一致しかつアサインされたユーザが存在しないタスクを取得し、
    ・ステータス（TODO-DOING-DONE）
    ・優先度（HIGH-MEDIUM-LOW）
    で並び替えて返却する。
    """
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
        .order_by(Task.status, Task.priority)
        .all()
    )


def find_by_statuses_and_priorities_by_pagination(
    filtering_statuses: List[Status],
    filtering_priorities: List[Priority],
    db: Session,
    params: Params,
) -> Tuple[List[Task], int]:
    return (
        db.query(Task)
        .filter(
            Task.status.in_(filtering_statuses), Task.priority.in_(filtering_priorities)
        )
        .limit(params.size)
        .offset(params.size * params.page)
        .all(),
        db.query(func.count(Task.id).label("total"))
        .filter(
            Task.status.in_(filtering_statuses), Task.priority.in_(filtering_priorities)
        )
        .first()
        .total,
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

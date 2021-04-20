from entities import User, TaskAssignment, Task
from entities.task import Status, Priority
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, cast, Optional, TypedDict
from exceptions import *


def find_all(db: Session) -> List[User]:
    return db.query(User).all()  # noqa


def find_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).get(user_id)
    if user is None:
        raise ApplicationException(ErrorMessages.UserIsNotFound)
    user = cast(User, user)
    return user


def find_by_username(db: Session, username: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    return user


def create(db: Session, username: str, password_hash: str) -> User:
    created_user = User(username=username, password_hash=password_hash)
    db.add(created_user)
    return created_user


def delete(db: Session, deleted_user: User) -> None:
    db.delete(deleted_user)


def get_users_with_doing_task_count_group_by_priority(
    db: Session,
) -> List[
    TypedDict(
        "UserWithDoingTaskCount",
        {"user_id": int, "user": User, "priority": Priority, "doing_task_count": int},
    )
]:
    users_with_doing_task_count_by_priority = (
        db.query(
            User,
            Task.priority,
            func.count(TaskAssignment.user_id).label("doing_task_count"),
        )
        .join(TaskAssignment, User.id == TaskAssignment.user_id)
        .join(Task, TaskAssignment.task_id == Task.id)
        .filter(Task.status != Status.DONE)
        .group_by(User.id, Task.priority)
        .order_by(User.id)
        .all()
    )

    return list(
        map(
            lambda result: {
                "user_id": result.User.id,
                "user": result.User,
                "priority": result.priority,
                "doing_task_count": result.doing_task_count,
            },
            users_with_doing_task_count_by_priority,
        )
    )


def get_users_with_done_task_count_order_by_done_task_count(
    db: Session,
) -> List[TypedDict("UserWithDoneTaskCount", {"user": User, "done_task_count": int})]:
    users_with_count_of_done_tasks = (
        db.query(
            User,
            func.count(TaskAssignment.user_id).label("done_task_count"),
        )
        .join(TaskAssignment)
        .join(Task)
        .filter(Task.status == Status.DONE)
        .group_by(User.id)
        .order_by(desc("done_task_count"))
        .all()
    )

    return list(
        map(
            lambda result: {
                "user": result.User,
                "done_task_count": result.done_task_count,
            },
            users_with_count_of_done_tasks,
        )
    )

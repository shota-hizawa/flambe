from repositories import user_repository
from sqlalchemy.orm import Session
from utils.crypt import encrypt
from typing import List, cast
from entities import User, Task
from entities.task import Status, Priority
from exceptions import *
from utils.sort import sort_tasks_by_priority


def get_all(db: Session) -> List[User]:
    return user_repository.find_all(db=db)


def get_incomplete_tasks(db: Session, user_id: int) -> List[Task]:
    user = get_user_by_id(db=db, user_id=user_id)

    doing_tasks = sort_tasks_by_priority(
        list(filter(lambda task: task.status is Status.DOING, user.tasks))
    )
    todo_tasks = sort_tasks_by_priority(
        list(filter(lambda task: task.status is Status.TODO, user.tasks))
    )
    return [*doing_tasks, *todo_tasks]


def get_doing_task_data_of_all_users(db: Session) -> List[dict]:
    users = user_repository.find_all(db=db)
    user_with_doing_task_data_list = []

    for user in users:
        doing_tasks = list(filter(lambda task: task.status is Status.DOING, user.tasks))
        high_task_count = len(
            list(
                filter(
                    lambda doing_task: doing_task.priority is Priority.HIGH,
                    doing_tasks,
                )
            )
        )
        medium_task_count = len(
            list(
                filter(
                    lambda doing_task: doing_task.priority is Priority.MEDIUM,
                    doing_tasks,
                )
            )
        )
        low_task_count = len(
            list(
                filter(
                    lambda doing_task: doing_task.priority is Priority.LOW,
                    doing_tasks,
                )
            )
        )
        user_with_doing_task_data_list.append(
            {
                "user": user,
                "doing_task_data": {
                    "high_task_count": high_task_count,
                    "medium_task_count": medium_task_count,
                    "low_task_count": low_task_count,
                },
            }
        )
    return user_with_doing_task_data_list


def generate_ranking_of_done_task_count(
    db: Session,
) -> List[dict]:
    users = user_repository.find_all(db=db)
    done_task_count_user_dictionaries = []
    for user in users:
        done_task_count_user_dictionaries.append(
            {
                "user": user,
                "done_task_count": len(
                    list(filter(lambda task: task.status is Status.DONE, user.tasks))
                ),
            }
        )

    # タスク数の降順でソート
    sorted_done_task_count_user_dictionaries = sorted(
        done_task_count_user_dictionaries,
        key=lambda x: x["done_task_count"],
        reverse=True,
    )

    ranking_of_done_task_count = []
    for index, dictionary in enumerate(sorted_done_task_count_user_dictionaries):
        rank = index + 1
        ranking_of_done_task_count.append(
            {
                "rank": rank,
                "user": dictionary["user"],
                "done_task_count": dictionary["done_task_count"],
            }
        )
    return ranking_of_done_task_count


def create(db: Session, username: str, password: str) -> User:
    if user_repository.find_by_username(db=db, username=username) is not None:
        raise ApplicationException(ErrorMessages.DuplicateUserName)

    password_hash = encrypt(password)
    created_user = user_repository.create(
        db=db, username=username, password_hash=password_hash
    )
    db.commit()
    return created_user


def delete(db, user_id: int):
    user = get_user_by_id(db=db, user_id=user_id)
    user = cast(User, user)
    user_repository.delete(db, user)
    db.commit()


def get_user_by_id(db, user_id: int) -> User:
    user = user_repository.find_by_id(db=db, user_id=user_id)
    if user is not None:
        return cast(User, user)
    else:
        raise ApplicationException(ErrorMessages.UserIsNotFound)

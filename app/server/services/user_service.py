from repositories import user_repository
from repositories import task_repository
from sqlalchemy.orm import Session
from utils.crypt import encrypt
from typing import List, cast
from entities import User, Task
from entities.task import Status, Priority
from exceptions import *


def get_all(db: Session) -> List[User]:
    return user_repository.find_all(db=db)


def get_incomplete_tasks(db: Session, user_id: int) -> List[Task]:
    return task_repository.find_by_user_id_and_status_order_by_status_asc_and_priority_desc(
        user_id=user_id, filtering_statuses=[Status.TODO, Status.DOING], db=db
    )


def get_doing_task_data_of_all_users(db: Session) -> List[dict]:
    users_with_doing_task_count_by_priority = (
        user_repository.get_users_with_doing_task_count_group_by_priority(db=db)
    )
    users = get_all(db)

    results_by_users = {}
    for user in users:
        results_by_users[user.id] = []

    for result in users_with_doing_task_count_by_priority:
        results_by_users[result["user_id"]].append(result)

    user_with_doing_task_data_list = []
    for user in users:
        high_task_count = 0
        medium_task_count = 0
        low_task_count = 0

        for result_related_user in results_by_users[user.id]:
            if result_related_user["priority"] == Priority.HIGH:
                high_task_count = result_related_user["doing_task_count"]
            if result_related_user["priority"] == Priority.MEDIUM:
                medium_task_count = result_related_user["doing_task_count"]
            if result_related_user["priority"] == Priority.LOW:
                low_task_count = result_related_user["doing_task_count"]

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
    users_with_done_task_count = (
        user_repository.get_users_with_done_task_count_order_by_done_task_count(db=db)
    )

    ranking_of_done_task_count = []
    for index, user_with_done_task_count in enumerate(users_with_done_task_count):
        rank = index + 1
        ranking_of_done_task_count.append(
            {
                "rank": rank,
                "user": user_with_done_task_count["user"],
                "done_task_count": user_with_done_task_count["done_task_count"],
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

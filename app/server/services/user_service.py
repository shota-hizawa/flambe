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
    return task_repository.find_by_user_id_and_status_order_by_status_and_priority(
        user_id=user_id, filtering_statuses=[Status.TODO, Status.DOING], db=db
    )


def get_doing_task_data_of_all_users(db: Session) -> List[dict]:
    """
    全ユーザと、それぞれの未完了タスク数を優先度別で集計したデータを返却する。
    """
    users = get_all(db=db)
    users_with_doing_task_count_by_priority = (
        user_repository.get_user_ids_with_doing_task_count_group_by_priority(db=db)
    )

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
    """
    全ユーザと、それぞれの完了タスク数を集計したデータを返却する。
    """

    # 0. ユーザ一覧をユーザIDをキーとした辞書に変換
    users = get_all(db=db)
    users_key_by_user_id = {}
    for user in users:
        users_key_by_user_id[user.id] = user

    user_ids_with_done_task_count = (
        user_repository.get_user_ids_with_done_task_count_order_by_done_task_count(
            db=db
        )
    )

    ranking_of_done_task_count = []
    rank = 1
    # 1. 完了タスクがあるユーザから結果データに格納していく
    for index, user_id_with_done_task_count in enumerate(user_ids_with_done_task_count):
        user_id = user_id_with_done_task_count["user_id"]
        ranking_of_done_task_count.append(
            {
                "rank": rank,
                "user": users_key_by_user_id[user_id],
                "done_task_count": user_id_with_done_task_count["done_task_count"],
            }
        )
        rank += 1
        users_key_by_user_id.pop(user_id)

    # 2. 完了タスクがないユーザを結果データに格納する（順不同）
    for user_without_done_task in users_key_by_user_id.values():
        ranking_of_done_task_count.append(
            {
                "rank": rank,
                "user": user_without_done_task,
                "done_task_count": 0,
            }
        )
        rank += 1

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

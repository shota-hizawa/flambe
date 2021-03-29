from entities import User
from sqlalchemy.orm import Session
from typing import List, cast
from exceptions import *


def find_all(db: Session) -> List[User]:
    return db.query(User).all()  # noqa


def find_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).get(user_id)
    if user is None:
        raise ApplicationException(ErrorMessages.UserIsNotFound)
    user = cast(User, user)
    return user


def create(db: Session, username: str, password_hash: str) -> User:
    created_user = User(username=username, password_hash=password_hash)
    db.add(created_user)
    return created_user


def delete(db: Session, deleted_user: User) -> None:
    db.delete(deleted_user)

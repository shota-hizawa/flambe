from entities import User
from sqlalchemy.orm import Session
from typing import List
from exceptions import *


def find_all(db: Session) -> List[User]:
    return db.query(User).filter(User.deleted == False).all()  # noqa


# soft_deleteをどうにかする方法を考える
def find_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).get(user_id)
    if user is None:
        raise ApplicationException(ErrorMessages.UserIsNotFound)
    return user


def create(db: Session, username: str, password_hash: str) -> User:
    created_user = User(username=username, password_hash=password_hash)
    db.add(created_user)
    return created_user


def soft_delete(deleted_user: User):
    deleted_user.deleted = True

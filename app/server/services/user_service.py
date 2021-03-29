from repositories import user_repository
from sqlalchemy.orm import Session
from utils.crypt import encrypt
from typing import List, cast
from entities import User
from exceptions import *


def get_all(db: Session) -> List[User]:
    return user_repository.find_all(db=db)


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

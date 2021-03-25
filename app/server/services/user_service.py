from repositories import user_repository
from sqlalchemy.orm import Session
from utils.crypt import encrypt
from typing import List, cast
from entities import User


def get_all(db: Session) -> List[User]:
    return user_repository.find_all(db=db)


def create(db: Session, username: str, password: str) -> User:
    password_hash = encrypt(password)
    created_user = user_repository.create(
        db=db, username=username, password_hash=password_hash
    )
    db.commit()
    return created_user


def delete(db, user_id: int):
    user = user_repository.find_by_id(db=db, user_id=user_id)
    if user is not None:
        user = cast(User, user)
        user_repository.soft_delete(user)
    else:
        raise Exception("user not found.")
    db.commit()

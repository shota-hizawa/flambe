from entities import User
from sqlalchemy.orm import Session
from typing import List


def find_all(db: Session) -> List[User]:
    return db.query(User).filter(User.deleted == False).all()  # noqa


def find_by_id(db: Session, user_id: int) -> User:
    return db.query(User).get(user_id)


def create(db: Session, username: str, password_hash: str) -> User:
    created_user = User(username=username, password_hash=password_hash)
    db.add(created_user)
    return created_user


def soft_delete(deleted_user: User):
    deleted_user.deleted = True

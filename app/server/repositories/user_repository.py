from entities import User
from sqlalchemy.orm import Session
from typing import List


def find_all(db: Session) -> List[User]:
    return db.query(User).filter(User.deleted == False).all()  # noqa


def create(db: Session, username: str, password_hash: str) -> User:
    created_user = User(username=username, password_hash=password_hash)
    db.add(created_user)
    return created_user


def soft_delete(db: Session, id: int):
    deleted_user = db.query(User).get(id)
    if deleted_user is not None:
        deleted_user.deleted = True

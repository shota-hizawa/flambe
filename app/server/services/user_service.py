from repositories import user_repository
from sqlalchemy.orm import Session
from utils.crypt import encrypt


def get_all(db: Session):
    return user_repository.find_all(db=db)


def create(db: Session, username: str, password: str):
    password_hash = encrypt(password)
    created_user = user_repository.create(db, username, password_hash)
    db.commit()
    return created_user


def delete(db, user_id: int):
    user_repository.soft_delete(db, user_id)
    db.commit()

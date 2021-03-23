from models import User
from sqlalchemy.orm import Session


def read_users(db: Session):
    items = db.query(User).filter(User.deleted == False).all()  # noqa
    return items

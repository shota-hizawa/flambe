from models.base import BaseModel
from sqlalchemy import Column, String


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(255), unique=True, nullable=False, comment="ユーザ名")

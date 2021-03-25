from entities.base import BaseModel
from sqlalchemy import Column, String


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(255), unique=True, nullable=False, comment="ユーザ名")
    password_hash = Column(String(128), nullable=False, comment="パスワードのハッシュ値")

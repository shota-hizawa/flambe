from entities.base import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from entities.task_assignment import TaskAssignment


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = {"mysql_engine": "InnoDB"}

    username = Column(String(255), unique=True, nullable=False, comment="ユーザ名")
    password_hash = Column(String(128), nullable=False, comment="パスワードのハッシュ値")
    tasks = relationship(
        "Task",
        secondary=TaskAssignment.__tablename__,
        back_populates="assignees",
    )

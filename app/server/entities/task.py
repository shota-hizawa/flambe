from entities.base import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as DbEnum
from enum import Enum
from entities.task_assignment import TaskAssignment
from typing import List


class Status(str, Enum):
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"


class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Task(BaseModel):
    __tablename__ = "tasks"
    __table_args__ = {"mysql_engine": "InnoDB"}

    title = Column(String(255), nullable=False, comment="タイトル")
    description = Column(String(255), comment="説明本文")
    status = Column(
        DbEnum(Status), nullable=False, default=Status.TODO, comment="ステータス"
    )
    priority = Column(
        DbEnum(Priority), nullable=False, default=Priority.MEDIUM, comment="優先度"
    )
    assignees = relationship(
        "User",
        secondary=TaskAssignment.__tablename__,
        back_populates="tasks",
    )

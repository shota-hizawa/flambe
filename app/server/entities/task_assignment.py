from entities.base import BaseModel
from sqlalchemy import INTEGER, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class TaskAssignment(BaseModel):
    __tablename__ = "task_assignments"
    __table_args__ = (
        UniqueConstraint("task_id", "user_id"),
        {"mysql_engine": "InnoDB"},
    )

    task_id = Column(INTEGER, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(INTEGER, ForeignKey("users.id"), nullable=False)

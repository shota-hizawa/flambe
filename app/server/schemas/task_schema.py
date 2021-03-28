from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional
from entities.task import Status, Priority


class TaskSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: Status
    priority: Priority
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateTaskSchema(BaseModel):
    title: constr(min_length=1, max_length=255)
    description: Optional[constr(min_length=0, max_length=255)]


class UpdateTaskStatusSchema(BaseModel):
    new_status: Status


class UpdateTaskPrioritySchema(BaseModel):
    new_priority: Priority

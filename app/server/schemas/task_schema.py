from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional, List
from entities.task import Status, Priority
from schemas.user_schema import UserSchemaInDB


class TaskSchemaInDB(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: Status
    priority: Priority
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TaskSchema(TaskSchemaInDB):
    assignees: List[UserSchemaInDB]


class CreateTaskSchema(BaseModel):
    title: constr(min_length=1, max_length=255)
    description: Optional[constr(min_length=0, max_length=255)]


class UpdateTaskStatusSchema(BaseModel):
    new_status: Status


class UpdateTaskPrioritySchema(BaseModel):
    new_priority: Priority


class AssignTaskSchema(BaseModel):
    task_id: int
    user_id: int


class RemoveAssignmentTaskSchema(BaseModel):
    task_id: int
    user_id: int

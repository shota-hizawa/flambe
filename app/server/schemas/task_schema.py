from fastapi_camelcase import CamelModel
from pydantic import constr
from datetime import datetime
from typing import Optional, List
from entities.task import Status, Priority
from schemas.user_schema import UserSchemaInDB


class TaskSchemaInDB(CamelModel):
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


class CreateTaskSchema(CamelModel):
    title: constr(min_length=1, max_length=255)
    description: Optional[constr(min_length=0, max_length=255)]
    priority: Priority


class UpdateTaskStatusSchema(CamelModel):
    new_status: Status


class UpdateTaskPrioritySchema(CamelModel):
    new_priority: Priority


class AssignTaskSchema(CamelModel):
    task_id: int
    user_id: int


class RemoveAssignmentTaskSchema(CamelModel):
    task_id: int
    user_id: int

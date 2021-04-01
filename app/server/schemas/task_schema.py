from fastapi_camelcase import CamelModel
from pydantic import constr
from typing import Optional, List
from entities.task import Status, Priority
from schemas.user_schema import UserSchemaInDB
from schemas.db_schema import TaskSchemaInDB


class TaskSchema(TaskSchemaInDB):
    assignees: List[UserSchemaInDB]


class CreateTaskSchema(CamelModel):
    title: constr(min_length=1, max_length=255)
    description: Optional[constr(min_length=0, max_length=255)]
    priority: Priority


class GetTasksFilteredByStatusAndPrioritySchema(CamelModel):
    statuses: List[Status]
    priorities: List[Priority]


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

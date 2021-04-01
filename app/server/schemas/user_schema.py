from pydantic import constr
from fastapi_camelcase import CamelModel
from schemas.db_schema import UserSchemaInDB, TaskSchemaInDB
from typing import List


class CreateUserSchema(CamelModel):
    username: constr(min_length=4, max_length=100)
    password: constr(min_length=8, max_length=100)


class DoingTaskDataSchema(CamelModel):
    high_task_count: int
    medium_task_count: int
    low_task_count: int
    tasks: List[TaskSchemaInDB]


class UserWithDoingTaskDataSchema(CamelModel):
    user: UserSchemaInDB
    doing_task_data: DoingTaskDataSchema

    class Config:
        orm_mode = True


class RankingOfDoneTaskCountSchema(CamelModel):
    rank: int
    user: UserSchemaInDB
    done_task_count: int

    class Config:
        orm_mode = True

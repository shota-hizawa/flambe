from pydantic import constr
from fastapi_camelcase import CamelModel


class UserSchemaInDB(CamelModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class CreateUserSchema(CamelModel):
    username: constr(min_length=1, max_length=255)
    password: constr(min_length=8, max_length=255)


class DoingTaskDataSchema(CamelModel):
    high_task_count: int
    medium_task_count: int
    low_task_count: int


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

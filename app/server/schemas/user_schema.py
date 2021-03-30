from pydantic import BaseModel, constr


class UserSchemaInDB(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class CreateUserSchema(BaseModel):
    username: constr(min_length=1, max_length=255)
    password: constr(min_length=8, max_length=255)


class DoingTaskDataSchema(BaseModel):
    high_task_count: int
    medium_task_count: int
    low_task_count: int


class UserWithDoingTaskDataSchema(BaseModel):
    user: UserSchemaInDB
    doing_task_data: DoingTaskDataSchema

    class Config:
        orm_mode = True


class RankingOfDoneTaskCountSchema(BaseModel):
    rank: int
    user: UserSchemaInDB
    done_task_count: int

    class Config:
        orm_mode = True

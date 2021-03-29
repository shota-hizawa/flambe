from pydantic import BaseModel, constr
from datetime import datetime


class UserSchemaInDB(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class CreateUserSchema(BaseModel):
    username: constr(min_length=1, max_length=255)
    password: constr(min_length=8, max_length=255)

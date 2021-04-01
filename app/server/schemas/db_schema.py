from fastapi_camelcase import CamelModel
from typing import Optional
from datetime import datetime
from entities.task import Status, Priority


class UserSchemaInDB(CamelModel):
    id: int
    username: str

    class Config:
        orm_mode = True


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

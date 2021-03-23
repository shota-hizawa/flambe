from pydantic import BaseModel
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

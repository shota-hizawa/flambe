from entities.user import User
from pydantic import BaseModel


class DoingTaskData(BaseModel):
    high_task_count: int
    medium_task_count: int
    low_task_count: int


class UserWithDoingTaskData:
    user: User
    doing_task_data: DoingTaskData

    def __init__(self, user: User, doing_task_data: DoingTaskData):
        self.user = user
        self.doing_task_data = doing_task_data

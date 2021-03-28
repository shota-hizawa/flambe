from abc import ABCMeta


class BaseMessage(metaclass=ABCMeta):

    text: str

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessages:
    class UserIsNotFound(BaseMessage):
        text = "指定されたユーザは存在しないか、すでに削除されています"

    class TaskIsNotFound(BaseMessage):
        text = "指定されたタスクは存在しないか、すでに削除されています"

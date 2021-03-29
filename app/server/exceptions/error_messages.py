from abc import ABCMeta


class BaseMessage(metaclass=ABCMeta):

    text: str

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessages:
    ############################################################
    # User系
    ############################################################
    class UserIsNotFound(BaseMessage):
        text = "指定されたユーザは存在しないか、すでに削除されています"

    class DuplicateUserName(BaseMessage):
        text = "同じ名前のユーザがすでに存在しています"

    ############################################################
    # Task系
    ############################################################
    class TaskIsNotFound(BaseMessage):
        text = "指定されたタスクは存在しないか、すでに削除されています"

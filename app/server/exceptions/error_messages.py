from abc import ABCMeta


class BaseMessage(metaclass=ABCMeta):

    text: str

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessages:
    ############################################################
    # システムエラー
    ############################################################
    class InternalServerError(BaseMessage):
        text = "システムエラーが発生しました、管理者に問い合わせてください"

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

    class UserIsNotAssignedToTheTask(BaseMessage):
        text = "指定されたユーザは、そのタスクに割り当てられていません"

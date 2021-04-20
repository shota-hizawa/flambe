from fastapi import status, HTTPException
from exceptions.error_messages import BaseMessage
from typing import Type


class ApplicationException(HTTPException):
    default_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self, error: Type[BaseMessage], status_code: int = default_status_code
    ) -> None:
        self.status_code = status_code
        self.detail = {
            "error_code": str(error()),
            "error_msg": error.text,
        }
        super().__init__(self.status_code, self.detail)

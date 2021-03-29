import traceback
from fastapi import status, HTTPException
from exceptions.error_messages import ErrorMessages


class InternalServerException(HTTPException):
    def __init__(self, e: Exception) -> None:
        self.exc = e
        self.stack_trace = traceback.format_exc()
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = [
            {
                "error_code": str(ErrorMessages.InternalServerError()),
                "error_msg": ErrorMessages.InternalServerError().text,
            }
        ]
        super().__init__(self.status_code, self.detail)

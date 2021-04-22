from fastapi import FastAPI, APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from controllers.user_controller import router as user_router
from controllers.task_controller import router as task_router
from exceptions import ApplicationException
from exceptions.system_exception import InternalServerException
from starlette.requests import Request


router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(task_router, prefix="/tasks", tags=["tasks"])


app = FastAPI()
app.include_router(router)

origins = ["http://localhost:9000"]


# cf. https://github.com/tiangolo/fastapi/issues/775#issuecomment-592946834
# noinspection PyBroadException
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        exception = InternalServerException(exc)
        return JSONResponse(status_code=exception.status_code, content=exception.detail)


app.middleware("http")(catch_exceptions_middleware)


# バリデーションエラーのハンドリング
# 1つ目のエラーのみ返却
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": {
                    "error_code": "ValidationError",
                    "error_msg": exc.errors()[0]["msg"],
                }
            }
        ),
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

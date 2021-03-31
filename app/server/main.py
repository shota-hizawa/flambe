from fastapi import FastAPI, APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from controllers.user_controller import router as user_router
from controllers.task_controller import router as task_router
from exceptions.system_exception import InternalServerException

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(task_router, prefix="/tasks", tags=["tasks"])


app = FastAPI()
app.include_router(router)

origins = ["http://localhost:9000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    exception = InternalServerException(exc)
    return JSONResponse(status_code=exception.status_code, content=exception.detail)


# バリデーションエラーのハンドリング
# 1つ目のエラーのみ返却
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"error_code": "ValidationError", "error_msg": exc.errors()[0]["msg"]}
        ),
    )

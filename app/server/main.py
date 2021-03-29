from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from controllers.user_controller import router as user_router
from controllers.task_controller import router as task_router
from exceptions.system_exception import InternalServerException

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(task_router, prefix="/tasks", tags=["tasks"])


app = FastAPI()
app.include_router(router)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    exception = InternalServerException(exc)
    return JSONResponse(status_code=exception.status_code, content=exception.detail)

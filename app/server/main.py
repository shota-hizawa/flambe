from fastapi import FastAPI, APIRouter
from controllers.user_controller import router as user_router
from controllers.task_controller import router as task_router

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(task_router, prefix="/tasks", tags=["tasks"])

app = FastAPI()
app.include_router(router)

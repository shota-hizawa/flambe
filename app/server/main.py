from fastapi import FastAPI, APIRouter
from controllers.user_controller import router as user_router

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["users"])

app = FastAPI()
app.include_router(router)

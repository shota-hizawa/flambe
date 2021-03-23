import uvicorn
from fastapi import FastAPI, APIRouter

router = APIRouter()

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

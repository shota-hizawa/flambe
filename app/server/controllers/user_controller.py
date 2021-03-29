from services import user_service
from database import get_db
from fastapi import APIRouter, Depends
from schemas.user_schema import UserSchemaInDB, CreateUserSchema
from schemas.task_schema import TaskSchemaInDB
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/", response_model=List[UserSchemaInDB])
async def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all(db)


@router.get("/{user_id}/tasks/incomplete", response_model=List[TaskSchemaInDB])
async def get_incomplete_tasks_assigned_to_user(
    user_id: int, db: Session = Depends(get_db)
):
    return user_service.get_incomplete_tasks(db=db, user_id=user_id)


@router.post("/", response_model=UserSchemaInDB)
async def create_user(
    create_user_schema: CreateUserSchema, db: Session = Depends(get_db)
):
    return user_service.create(
        db, create_user_schema.username, create_user_schema.password
    )


@router.delete("/{user_id}", response_model=None)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete(db, user_id)

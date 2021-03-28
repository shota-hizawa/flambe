from services import user_service
from database import get_db
from fastapi import APIRouter, Depends
from schemas.user_schema import UserSchema, CreateUserSchema
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def get_all(db: Session = Depends(get_db)):
    return user_service.get_all(db)


@router.post("/", response_model=UserSchema)
async def create(create_user_schema: CreateUserSchema, db: Session = Depends(get_db)):
    return user_service.create(
        db, create_user_schema.username, create_user_schema.password
    )


@router.delete("/{user_id}", response_model=None)
async def delete(user_id: int, db: Session = Depends(get_db)):
    user_service.delete(db, user_id)

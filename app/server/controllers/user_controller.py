from repositories import user_repository
from database import get_db
from fastapi import APIRouter, Depends
from schemas.user_schema import UserSchema, CreateUserSchema, DeleteUserSchema
from sqlalchemy.orm import Session
from typing import List
from utils.crypt import encrypt

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def get_all(db: Session = Depends(get_db)):
    return user_repository.find_all(db=db)


@router.post("/", response_model=UserSchema)
async def create(create_user_schema: CreateUserSchema, db: Session = Depends(get_db)):
    created_user = user_repository.create(
        db, create_user_schema.username, encrypt(create_user_schema.password)
    )
    db.commit()
    return created_user


@router.delete("/{user_id}", response_model=int)
async def soft_delete(user_id: int, db: Session = Depends(get_db)):
    user_repository.soft_delete(db, user_id)
    db.commit()

from repositories import user_repository
from database import get_db
from fastapi import APIRouter, Depends
from schemas.user_schema import UserSchema
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def read_users(db: Session = Depends(get_db)):
    return user_repository.read_users(db=db)

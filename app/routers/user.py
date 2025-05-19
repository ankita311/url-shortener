from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, utils, models, oauth2
from ..database import get_db

router = APIRouter(prefix="/user", tags = ['USER'])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    hash_pass = utils.hash(user.password)
    user.password = hash_pass
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/profile", response_model=schemas.UserOut)
def get_me(current_user: int = Depends(oauth2.get_current_user)):
    return current_user

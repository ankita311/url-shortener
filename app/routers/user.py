from fastapi import APIRouter, Depends, HTTPException, Response, status
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

@router.patch("/update", response_model=schemas.UserUpdateOut)
def update_user(updated_user: schemas.UserUpdate, 
                current_user: models.User = Depends(oauth2.get_current_user),
                db: Session = Depends(get_db)):
    
    user_query = db.query(models.User).filter(models.User.id == current_user.id)

    data = updated_user.model_dump(exclude_unset=True)

    # if "password" in data:
    #     data['password'] = utils.hash(data['password'])

    user_query.update(data, synchronize_session=False)
    db.commit()

    return user_query.first()

@router.put("/password")
def update_password(user_passwords: schemas.UserPasswords, 
                    current_user: models.User = Depends(oauth2.get_current_user),
                    db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    match = utils.verify(user_passwords.old_password, user.password)

    if not match:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password")
    
    user.password = utils.hash(user_passwords.new_password)
    db.commit()

    return {"msg": "successfully updated password"}

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: models.User = Depends(oauth2.get_current_user),
                db: Session = Depends(get_db)):
    
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
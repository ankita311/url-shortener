from typing import List
from fastapi import Depends, FastAPI
from . import database, oauth2, models, schemas
from .routers import user, auth, url
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from .scheduler import start_scheduler


#issues:
#1. fix token cleaning in db.


app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(url.router)

# @app.on_event("startup")
# def on_startup():
#     start_scheduler()


@app.get("/test")
def test(current_user: int = Depends(oauth2.get_current_user)):
    return current_user

@app.get('/dashboard', response_model= List[schemas.UrlInfo])
def dashboard(current_user: models.User = Depends(oauth2.get_current_user),
              db: Session = Depends(database.get_db)):
    
    urls = db.query(models.Url).filter(models.Url.owner_id == current_user.id).all()

    return urls
from fastapi import Depends, FastAPI
from . import database, oauth2, models
from .routers import user, auth, url
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from .scheduler import start_scheduler

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
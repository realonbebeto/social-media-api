from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router, prefix='/posts')
app.include_router(user.router, prefix='/users')
app.include_router(auth.router, prefix='/auth')

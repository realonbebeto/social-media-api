from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, like

# Not neccessary when alembic is setup
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router, prefix='/posts')
app.include_router(user.router, prefix='/users')
app.include_router(auth.router, prefix='/auth')
app.include_router(like.router, prefix='/like')

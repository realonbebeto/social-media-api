from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import *
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


my_posts = []


@app.get("/")
async def root():
    return {"message": "Hello, Bebeto"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(type(posts))
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"my_posts": new_post}


@app.get("/posts/latest")
async def get_post_latest(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()[-1]
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found")
    return {"post_detail": post}

# Paths with {} placeholders should come last when they have matching methods


@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=id)

    if post.first() == None:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, update_post: Post, db: Session = Depends(get_db)):
    post_q = db.query(models.Post).filter_by(id=id)

    if post_q.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    post_q.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_q.first()}

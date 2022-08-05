from operator import mod
from statistics import mode
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models
from ..database import get_db
from ..schemas import CreatePost, PostResponse, UpdatePost, GetPost
from ..oauth2 import getCurrentUser


router = APIRouter(tags=['Posts'])

#


@router.get("/", response_model=List[GetPost])
async def getAllPosts(db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    #posts = db.query(models.Post).all()

    posts = db.query(models.Post, func.count(models.Like.user_id).label("likes")).join(
        models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).all()

    if not posts:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found")
    return posts


@router.get("/find", response_model=List[GetPost])
async def search(db: Session = Depends(get_db), current_user=Depends(getCurrentUser), limit: int = 5, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Like.user_id).label("likes")).join(
        models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()

    if not posts:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found")
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def createPost(post: CreatePost, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest", response_model=GetPost)
async def getLatestPost(db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    post = db.query(models.Post, func.count(models.Like.user_id).label("likes")).join(
        models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).order_by(models.Post.created_at.desc()).first()
    print()
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found")

    if post.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    return post

# Paths with {} placeholders should come last when they have matching methods


@router.get("/{id}", response_model=GetPost)
async def getPostById(id: int, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    post = db.query(models.Post, func.count(models.Like.user_id).label("likes")).join(
        models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' not found")

    if post.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePostById(id: int, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    post_q = db.query(models.Post).filter_by(id=id)
    post = post_q.first()

    if post == None:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_q.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=GetPost)
async def updatePostById(id: int, update_post: UpdatePost, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    post_q = db.query(models.Post).filter_by(id=id)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_q.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return post_q.first()

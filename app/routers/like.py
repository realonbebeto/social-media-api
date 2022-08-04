from hashlib import new
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models
from ..database import get_db
from ..schemas import CreateLike
from ..oauth2 import getCurrentUser


router = APIRouter(tags=['Likes'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def effectLike(like: CreateLike, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post of id {like.post_id} not found")

    like_q = db.query(models.Like).filter(
        models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    found = like_q.first()
    if (like.direction == 1):
        if found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} already has like the post {like.post_id}")

        new_like = models.Like(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return {"detail": "liked"}
    else:
        if not found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")

        like_q.delete(synchronize_session=False)
        db.commit()
        return {"detail": "Unliked"}


# async def effectLike(like: CreateLike, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    # like_q = db.query(models.Like).filter_by(
        # post_id=like.post_id, user_id=current_user.id)
    #found_like = like_q.first()

    # if like.direction == 1:
        # if found_like:
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        # detail=f"User {current_user.id} already has like the post {like.post_id}")

       # new_like = models.Like(post_id=like.post_id,
        # user_id=current_user.id)
        # db.add(new_like)
        # db.commit()
        # db.refresh(new_like)
        # return {"detail": "Liked"}

    # else:
        # if not found_like:
        # raise HTTPException(
        # status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")

        # like_q.delete(synchronize_session=False)
        # db.commit()

        # return {"detail": "Like Undone"}

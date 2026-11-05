from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/v1/comments", tags=["Comments"])


@router.get("", response_model=List[schemas.CommentResponse])
def get_comments(
    task_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Comment)
    if task_id is not None:
        query = query.filter(models.Comment.task_id == task_id)
    return query.all()


@router.get("/{comment_id}", response_model=schemas.CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.post("", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(comment_in: schemas.CommentCreate, db: Session = Depends(get_db)):
    comment = models.Comment(**comment_in.model_dump())
    db.add(comment)
    try:
        db.commit()
        db.refresh(comment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid task_id or author_id")
    return comment


@router.patch("/{comment_id}", response_model=schemas.CommentResponse)
def update_comment(comment_id: int, comment_in: schemas.CommentUpdate, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    update_data = comment_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(comment, key, value)

    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    db.delete(comment)
    db.commit()
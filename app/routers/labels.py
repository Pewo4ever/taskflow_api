from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/v1/labels", tags=["Labels"])


@router.get("", response_model=List[schemas.LabelResponse])
def get_labels(db: Session = Depends(get_db)):
    return db.query(models.Label).all()


@router.get("/{label_id}", response_model=schemas.LabelResponse)
def get_label(label_id: int, db: Session = Depends(get_db)):
    label = db.query(models.Label).filter(models.Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
    return label


@router.post("", response_model=schemas.LabelResponse, status_code=status.HTTP_201_CREATED)
def create_label(label_in: schemas.LabelCreate, db: Session = Depends(get_db)):
    label = models.Label(**label_in.model_dump())
    db.add(label)
    try:
        db.commit()
        db.refresh(label)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Label with this name already exists")
    return label


@router.patch("/{label_id}", response_model=schemas.LabelResponse)
def update_label(label_id: int, label_in: schemas.LabelUpdate, db: Session = Depends(get_db)):
    label = db.query(models.Label).filter(models.Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")

    update_data = label_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(label, key, value)

    try:
        db.commit()
        db.refresh(label)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Label name conflict")
    return label


@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(label_id: int, db: Session = Depends(get_db)):
    label = db.query(models.Label).filter(models.Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
    db.delete(label)
    db.commit()
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/projects", tags=["Projects"])


@router.get("", response_model=List[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):

    logger.debug("Вызван эндпоинт для получения списка всех проектов")

    projects = db.query(models.Project).all()


    logger.info(f"Успешно получено проектов из базы: {len(projects)}")
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    logger.debug(f"Поиск проекта по ID: {project_id}")
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        logger.warning(f"Попытка запросить несуществующий проект с ID: {project_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project


@router.post("", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    logger.debug(f"Данные для создания проекта: {project_in.model_dump()}")
    try:
        project = models.Project(**project_in.model_dump())
        db.add(project)
        db.commit()
        db.refresh(project)

        logger.info(f"Успешно создан новый проект с ID: {project.id}")
        return project
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при создании проекта в базе данных: {e}")
        raise HTTPException(status_code=400, detail="Could not create project")


@router.patch("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(project_id: int, project_in: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        logger.warning(f"Попытка обновить несуществующий проект с ID: {project_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    update_data = project_in.model_dump(exclude_unset=True)
    logger.debug(f"Поля для обновления проекта {project_id}: {update_data}")

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    logger.info(f"Проект с ID {project_id} успешно обновлен")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        logger.warning(f"Попытка удалить несуществующий проект с ID: {project_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    db.delete(project)
    db.commit()

    logger.info(f"Проект с ID {project_id} был успешно удален")
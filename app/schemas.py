from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# --- USERS ---
class UserBase(BaseModel):
    email: EmailStr
    display_name: str = Field(..., max_length=255)
    role: str = Field(default="operator", pattern="^(operator|admin)$")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = Field(None, max_length=255)
    role: Optional[str] = Field(None, pattern="^(operator|admin)$")


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- PROJECTS ---
class ProjectBase(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- LABELS ---
class LabelBase(BaseModel):
    name: str = Field(..., max_length=64)
    color: str = Field(default="#6b7280", pattern="^#[0-9a-fA-F]{6}$")


class LabelCreate(LabelBase):
    pass


class LabelUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=64)
    color: Optional[str] = Field(None, pattern="^#[0-9a-fA-F]{6}$")


class LabelResponse(LabelBase):
    id: int

    class Config:
        from_attributes = True


# --- TASKS ---
class TaskBase(BaseModel):
    project_id: int
    assignee_id: Optional[int] = None
    label_id: Optional[int] = None
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    status: str = Field(default="open", pattern="^(open|in_progress|done)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    label_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(open|in_progress|done)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- COMMENTS ---
class CommentBase(BaseModel):
    task_id: int
    author_id: int
    body: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    body: Optional[str] = Field(None, min_length=1)


class CommentResponse(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
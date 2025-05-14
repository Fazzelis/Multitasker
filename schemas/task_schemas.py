from typing import Optional

from pydantic import BaseModel, conint, EmailStr
from uuid import UUID
from datetime import date


class TaskBase(BaseModel):
    name: str
    description: str
    due_date: date
    indicator: conint(ge=0, le=4)
    creator: UUID
    executor: EmailStr
    project_id: UUID


class TaskCreate(BaseModel):
    name: str
    description: str
    due_date: date
    indicator: conint(ge=0, le=4)
    executor_email: EmailStr
    project_id: UUID


class TaskPatch(BaseModel):
    task_id: UUID
    project_id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    indicator: Optional[conint(ge=0, le=4)] = 0
    executor_email: Optional[EmailStr] = None


class TaskDelete(BaseModel):
    task_id: UUID

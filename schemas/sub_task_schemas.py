from typing import Optional

from pydantic import BaseModel, EmailStr, conint
from datetime import date
from uuid import UUID


class SubTaskSchemas(BaseModel):
    name: str
    executor_email: EmailStr
    description: str
    due_date: date
    task_id: UUID
    indicator: conint(ge=0, le=4)


class SubTaskCreate(BaseModel):
    name: str
    executor_email: EmailStr
    description: str
    due_date: date
    task_id: UUID
    indicator: conint(ge=0, le=4)
    creator_id: UUID


class SubTaskInfo(SubTaskCreate):
    sub_task_id: UUID


class SubTaskGetDelete(BaseModel):
    id: UUID


class SubTaskPatch(BaseModel):
    sub_task_id: UUID
    name: Optional[str] = None
    executor_email: Optional[EmailStr] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    indicator: Optional[int] = None

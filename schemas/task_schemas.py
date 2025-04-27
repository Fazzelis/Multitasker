from pydantic import BaseModel
from uuid import UUID
from datetime import date


class TaskBase(BaseModel):
    name: str
    description: str
    due_date: date
    indicator: int
    executor: UUID


class TaskCreate(TaskBase):
    project_id: UUID


class TaskPatch(TaskBase):
    task_id: UUID


class TaskDelete(BaseModel):
    task_id: UUID

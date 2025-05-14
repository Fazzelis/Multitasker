from typing import List

from pydantic import BaseModel

from schemas.task_schemas import TaskBase, TaskWithSubTasks


class TaskResponse(BaseModel):
    status: str
    task: TaskBase


class MyTasksResponse(BaseModel):
    status: str
    tasks: List[TaskBase]


class ProjectTasksResponse(BaseModel):
    status: str
    tasks: List[TaskWithSubTasks]

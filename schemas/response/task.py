from pydantic import BaseModel
from schemas.task_schemas import *


class TaskResponse(BaseModel):
    status: str
    task: TaskBase

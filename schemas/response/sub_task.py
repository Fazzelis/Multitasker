from typing import List

from pydantic import BaseModel
from schemas.sub_task_schemas import SubTaskInfo, SubTaskSchemas


class SubTaskResponse(BaseModel):
    status: str
    sub_task: SubTaskInfo


class MySubTasks(BaseModel):
    status: str
    sub_tasks: List[SubTaskInfo]


class SubTaskCreateResponse(BaseModel):
    status: str
    sub_task: SubTaskSchemas


class SubTaskDeleteResponse(BaseModel):
    status: str
    detail: str

from pydantic import BaseModel
from schemas.sub_task_schemas import SubTaskInfo, SubTaskSchemas


class SubTaskResponse(BaseModel):
    status: str
    task: SubTaskInfo


class SubTaskCreateResponse(BaseModel):
    status: str
    task: SubTaskSchemas


class SubTaskDeleteResponse(BaseModel):
    status: str
    detail: str

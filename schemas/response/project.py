from pydantic import BaseModel
from schemas.project_schemas import *


class ProjectResponse(BaseModel):
    status: str
    project: ProjectDtoWithCategoryId


class ProjectResponseWithoutCategoryId(BaseModel):
    status: str
    project: ProjectDto

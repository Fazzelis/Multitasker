from typing import List

from pydantic import BaseModel

from schemas.project_schemas import ProjectDto, ProjectDtoInfo


class ProjectResponse(BaseModel):
    status: str
    project: ProjectDto


class AllProjectsResponse(BaseModel):
    status: str
    projects: List[ProjectDtoInfo]

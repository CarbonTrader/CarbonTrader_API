from pydantic import BaseModel

from app.Model.Project import Project


class CreateProjectRequest(BaseModel):
    auth_token: str
    new_project: Project
    email: str

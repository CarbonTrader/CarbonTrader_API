from pydantic import BaseModel
from app.Model.Project import Project
from typing import Union
from typing import List, Optional


# TODO: Correct attributes
class CreditProvider(BaseModel):
    name: str
    description: str
    projects: Optional[List['Project']] = None

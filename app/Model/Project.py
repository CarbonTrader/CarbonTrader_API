from pydantic import BaseModel
from app.Model.Credit import Credit
from typing import Union
from typing import List

#TODO: Correct attributes
class Project(BaseModel):
    project: str
    description: str
    image: str
    verifier: str
    sector: str
    evaluation_criteria: str
    quantification_methodology: str
    credits: Union[List[Credit],None] = None

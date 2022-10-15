from typing import List
from typing import Union

from pydantic import BaseModel

from app.Model.Credit import Credit


# TODO: Correct attributes
class Project(BaseModel):
    id: str
    name: str
    description: str
    images: Union[List[str], None]
    project_verifier: str
    sector: str
    evaluation_criteria: str
    quantification_methodology: Union[List[str], None]
    credits: Union[List[Credit], None] = None

    def __int__(self, p):
        self.id = str(p.id),
        self_name = p.name,
        self_description = p.description,
        self.images = p.images,
        self.project_verifier = p.project_verifier,
        self.sector = p.sector,
        self.evaluation_criteria = p.evaluation_criterio,
        self.quantification_methodology = p.quantification_methodology

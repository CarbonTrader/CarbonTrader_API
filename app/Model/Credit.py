from pydantic import BaseModel
from typing import Union

#TODO: Correct credits attributes
class Credit(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None





from pydantic import BaseModel
from typing import Union

#TODO: Correct attributes
class User(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
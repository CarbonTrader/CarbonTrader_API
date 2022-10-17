from typing import Union

from pydantic import BaseModel


# TODO: Correct credits attributes
class Credit(BaseModel):
    carbontrader_serial: Union[str, None]
    credit_provider_serial: str
    project_id: str
    price: int
    retire_date: Union[int, None]

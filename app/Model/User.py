from pydantic import BaseModel


# TODO: Correct attributes
class User(BaseModel):
    email: str
    name: str

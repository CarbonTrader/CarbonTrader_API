from pydantic import BaseModel


class SignUpRequest(BaseModel):
    name = ''
    email = ''
    password = ''
    role = ''

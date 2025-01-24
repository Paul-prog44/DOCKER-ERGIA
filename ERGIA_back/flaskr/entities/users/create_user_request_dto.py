from pydantic import BaseModel
import json

class CreateUserRequestDTO(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    acceptCgu: bool

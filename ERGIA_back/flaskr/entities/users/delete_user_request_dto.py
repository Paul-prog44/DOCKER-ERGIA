from pydantic import BaseModel


class DeleteUserRequestDTO(BaseModel):
    email: str

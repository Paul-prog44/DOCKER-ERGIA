from typing import Optional
from pydantic import BaseModel

class CreateScuRequestDTO(BaseModel):
    idea: str
    weight: Optional[int] = 0
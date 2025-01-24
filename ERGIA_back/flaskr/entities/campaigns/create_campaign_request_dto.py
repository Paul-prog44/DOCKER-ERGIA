from datetime import datetime
from typing import Optional

from pydantic import BaseModel
import json

class CreateCampaignRequestDTO(BaseModel):

    owner_id: int
    date_phase_1: Optional[datetime] = None
    date_phase_2: Optional[datetime] = None
    name: str
    status_id: Optional[int] = 1


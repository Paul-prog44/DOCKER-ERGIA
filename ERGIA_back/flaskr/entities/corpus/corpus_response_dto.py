from pydantic import BaseModel


class CorpusResponseDTO(BaseModel):
    id_original_text: int
    path: str
    campaign_id: int
from pydantic import BaseModel

class SummaryCreateRequest(BaseModel):
    user_id: int
    content: str
    image: str

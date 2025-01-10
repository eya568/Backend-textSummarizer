# Domain entities
from pydantic import BaseModel

class Text(BaseModel):
    content: str

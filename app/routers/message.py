from fastapi import APIRouter
from app.application.summarizer import Summarizer
from app.domain.entities import Text

router = APIRouter()
summarizer = Summarizer()

@router.post("/summarize")
async def summarize_text(text: Text):
    summary = summarizer.summarize(text.content)
    return {"summary": summary}
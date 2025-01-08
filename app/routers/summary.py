from fastapi import APIRouter
from app.domain.data.models import SessionLocal, Summary
from app.application.dtos.summary_request import SummaryCreateRequest

router = APIRouter()

@router.post("/add-summary")
async def add_summary(summary: SummaryCreateRequest):
    db = SessionLocal()
    try:
        # Create a Summary instance
        db_summary = Summary(user_id=summary.user_id, content=summary.content, image=summary.image)
        db.add(db_summary)
        db.commit()
        db.refresh(db_summary)
        return {"status": "Summary added successfully", "summary_id": db_summary.id}
    except Exception as e:
        db.rollback()
        return {"status": "Failed to add summary", "error": str(e)}
    finally:
        db.close()

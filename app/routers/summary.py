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

@router.get("/get-summary/{summary_id}")
async def get_summary(summary_id: int):
    db = SessionLocal()
    try:
        db_summary = db.query(Summary).filter(Summary.id == summary_id).first()
        if db_summary:
            return {"status": "Summary retrieved successfully", "summary": db_summary}
        else:
            return {"status": "Summary not found"}
    except Exception as e:
        return {"status": "Failed to retrieve summary", "error": str(e)}
    finally:
        db.close()

@router.get("/get-summaries")
async def get_summaries():
    db = SessionLocal()
    try:
        db_summaries = db.query(Summary).all()
        return {"status": "Summaries retrieved successfully", "summaries": db_summaries}
    except Exception as e:
        return {"status": "Failed to retrieve summaries", "error": str(e)}
    finally:
        db.close()
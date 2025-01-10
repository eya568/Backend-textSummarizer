from fastapi import APIRouter, HTTPException, status, Query
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
async def get_summaries(user_id: int = Query(..., description="User ID to filter summaries")):
    """
    Retrieve summaries filtered by the user ID.
    """
    db = SessionLocal()
    try:
        # Filter summaries by the provided user_id
        db_summaries = db.query(Summary).filter(Summary.user_id == user_id).all()
        return {"status": "Summaries retrieved successfully", "summaries": db_summaries}
    except Exception as e:
        return {"status": "Failed to retrieve summaries", "error": str(e)}
    finally:
        db.close()

@router.delete("/delete-summary/{summary_id}")
async def delete_summary(summary_id: int):
    db = SessionLocal()
    try:
        # Find the summary to delete
        db_summary = db.query(Summary).filter(Summary.id == summary_id).first()
        
        # If summary doesn't exist, raise a 404 error
        if not db_summary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Summary with ID {summary_id} not found"
            )
        
        # Delete the summary
        db.delete(db_summary)
        db.commit()
        
        return {
            "status": "Summary deleted successfully", 
            "summary_id": summary_id
        }
    except HTTPException:
        # Re-raise HTTPException to preserve its status code and detail
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Failed to delete summary: {str(e)}"
        )
    finally:
        db.close()
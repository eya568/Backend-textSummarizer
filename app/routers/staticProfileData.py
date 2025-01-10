from fastapi import APIRouter,HTTPException,status
from app.domain.data.models import SessionLocal, User, Summary
from sqlalchemy import func



router = APIRouter()



@router.get("/profile/{user_id}")
async def get_user_profile(user_id: int):
    db = SessionLocal()
    try:
        # Query to get user details
        user = db.query(User).filter(User.id == user_id).first()
        
        # Query to count user's summaries
        summary_count = db.query(func.count(Summary.id)).filter(Summary.user_id == user_id).scalar()
        
        # If user not found, raise an HTTP exception
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Return user profile data
        return {
            "username": user.username,
            "email": user.email,
            "summary_count": summary_count
        }
    finally:
        db.close()


@router.delete("/delete_account/{user_id}")
async def delete_account(user_id: int):
    db = SessionLocal()
    try:
        # First, check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        
        # If user not found, raise 404 error
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Delete all summaries associated with the user
        db.query(Summary).filter(Summary.user_id == user_id).delete()
        
        # Delete the user
        db.query(User).filter(User.id == user_id).delete()
        
        # Commit the changes
        db.commit()
        
        return {
            "status": "success", 
            "message": f"User {user_id} and their associated summaries have been deleted"
        }
    except Exception as e:
        # Rollback in case of any error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the account: {str(e)}"
        )
    finally:
        db.close()

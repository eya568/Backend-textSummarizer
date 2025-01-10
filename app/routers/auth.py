from fastapi import APIRouter,HTTPException,status
from datetime import timedelta
from app.domain.data.models import SessionLocal, User
from passlib.context import CryptContext
import jwt

from app.application.dtos.login_request import LoginRequest
from typing import List

from datetime import datetime, timedelta
# JWT configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter()

@router.post("/login")
async def login_user(user: LoginRequest):
    db = SessionLocal()
    try:
        # Verify user
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create JWT token with user ID and email
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": db_user.email, 
                "user_id": db_user.id
            }, 
            expires_delta=access_token_expires
        )
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "user_id": db_user.id
        }
    except HTTPException as e:
        raise e
    finally:
        db.close()

@router.get("/accounts", response_model=List[dict])
async def get_all_accounts():
    db = SessionLocal()
    try:
        # Query all users from the database
        users = db.query(User).all()

        # Return a list of user data (excluding sensitive information)
        user_list = [
            {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,  # Include relevant fields
            }
            for user in users
        ]
        return user_list
    except Exception as e:
        return {"status": "Failed", "error": str(e)}
    finally:
        db.close()
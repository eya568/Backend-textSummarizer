from fastapi import APIRouter
from datetime import timedelta
from app.domain.data.models import SessionLocal, User
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel
from app.application.dtos.login_request import LoginRequest

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
            return {"status": "Failed", "error": "Invalid credentials"}

        # Create JWT token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}
    finally:
        db.close()

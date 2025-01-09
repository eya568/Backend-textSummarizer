from fastapi import APIRouter
from app.domain.data.models import SessionLocal, User
from passlib.context import CryptContext
from app.application.dtos.register_request import RegisterRequest

router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register")
async def register_user(user: RegisterRequest):
    db = SessionLocal()
    
    try:
        
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            print(user.email)
            return {"status": "Failed to register user", "error": "Email already exists"}

        # Hash the password
        hashed_password = get_password_hash(user.password)

        # Create a User instance
        db_user = User(username=user.username, email=user.email, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"status": "User registered successfully", "user_id": db_user.id}
    except Exception as e:
        db.rollback()
        return {"status": "Failed to register user", "error": str(e)}
    finally:
        db.close()

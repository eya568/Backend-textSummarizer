from fastapi import APIRouter, HTTPException, status
from app.domain.data.models import SessionLocal, User
from passlib.context import CryptContext
from app.application.dtos.register_request import RegisterRequest
import smtplib
router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterRequest):
    db = SessionLocal()
    
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Email already exists"
            )

        # Hash the password
        hashed_password = get_password_hash(user.password)

        # Create a User instance
        db_user = User(username=user.username, email=user.email, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_password = "fagd dmse rjxr fuju"  # App password for Gmail

    # Prepare email content
        subject = "Thank You for Joining Our Platform!"
        body = f"""Subject: {subject}

        Thank you for creating an account on textSummarizer! We're thrilled to have you as part of our community.

        

        If you have any questions or need assistance, feel free to reach out to our support team at abdallahbenselam@gmail.com / swayedaya@gmail.com.
        Welcome aboard! 
        Best regards,
        The TextSummarizer Team"""

        try:
        # Establish SMTP connection
          server = smtplib.SMTP(smtp_server, smtp_port)
          server.starttls()
          server.login("abdallahbenselam@gmail.com", sender_password)
        
          # Send email
          server.sendmail("abdallahbenselam@gmail.com", user.email, body)
          server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
        return {
            "message": "User registered successfully", 
            "user_id": db_user.id
        }
    except HTTPException:
        # Re-raise HTTPException to preserve its status code and detail
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to register user"
        )
    finally:
        db.close()

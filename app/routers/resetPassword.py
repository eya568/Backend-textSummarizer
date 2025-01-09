from fastapi import APIRouter, Depends, HTTPException, status
import smtplib
import secrets
from datetime import datetime, timedelta
from app.domain.data.models import SessionLocal, User
from pydantic import BaseModel
from passlib.context import CryptContext
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Temporary in-memory storage for reset tokens (replace with database in production)
reset_tokens = {}
# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

def generate_reset_token(email: str) -> str:
    """Generate a secure reset token for the given email."""
    token = secrets.token_urlsafe(32)
    reset_tokens[token] = {
        'email': email,
        'created_at': datetime.utcnow(),
        'used': False
    }
    return token

def send_reset_email(sender_email: str, receiver_email: str, reset_link: str):
    """Send password reset email with a secure link using specified SMTP method."""
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_password = "fagd dmse rjxr fuju"  # App password for Gmail

    # Prepare email content
    subject = "Password Reset Request"
    body = f"""Subject: {subject}

You have requested to reset your password. 
Click the link below to reset your password:

{reset_link}

This link will expire in 1 hour.
If you did not request a password reset, please ignore this email."""

    try:
        # Establish SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        server.sendmail(sender_email, receiver_email, body)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@router.post("/request-password-reset")
def request_password_reset(request: PasswordResetRequest):
    """
    Request a password reset by sending a reset link to the user's email.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User with this email does not exist"
            )
        
        # Generate reset token
        reset_token = generate_reset_token(request.email)
        
        # Construct reset link (replace with your frontend URL)
        reset_link = f"http://localhost:5173/reset-password?token={reset_token}"
        
        # Send reset email
        sender_email = "abdallahbenselam@gmail.com"
        email_sent = send_reset_email(sender_email, request.email, reset_link)
        
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Failed to send password reset email"
            )
        
        return {"message": "Password reset link sent to your email"}
    
    finally:
        # Always close the database session
        db.close()

@router.post("/reset-password")
def reset_password(request: PasswordResetConfirm):
    """
    Confirm password reset using the token from the email.
    """
    # Create a database session
    db = SessionLocal()
    
    try:
        # Validate token
        token_info = reset_tokens.get(request.token)
        
        if not token_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid or expired reset token"
            )
        
        # Check token expiration (1 hour)
        if (datetime.utcnow() - token_info['created_at']) > timedelta(hours=1):
            del reset_tokens[request.token]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Reset token has expired"
            )
        
        # Check if token has been used
        if token_info['used']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Token has already been used"
            )
        
        # Find user
        user = db.query(User).filter(User.email == token_info['email']).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        
        # Update password (ensure to hash the password)
        hashed_password = get_password_hash(request.new_password)   # Replace with proper password hashing
        user.password = hashed_password
        db.commit()
        
        # Mark token as used
        token_info['used'] = True
        
        return {"message": "Password reset successfully"}
    
    finally:
        # Always close the database session
        db.close()
from fastapi import APIRouter
from app.domain.data.models import SessionLocal, User
from app.application.dtos.register_request import RegisterRequest
import smtplib


router = APIRouter()





@router.post("/reset-password")
async def register_user():
    email = input("Sender EMail  : ")
    reeiver_mail = input("Receiver EMail : ")
    subject = input("Subject : ")
    message = input("Message : ")
    text = "Subject: {}\n\n{}".format(subject, message)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, "fagd dmse rjxr fuju")
    
    server.sendmail(email, reeiver_mail, text)
    print("Mail Sent HEHEHE" + reeiver_mail )
from fastapi import FastAPI
from app.routers import message

app = FastAPI()

app.include_router(message.router)

from fastapi import FastAPI
from app.routers import message
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import  test_connection
from fastapi import Depends
from sqlalchemy import text

app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(message.router)


@app.post("/test-connection")
async def test_db_connection():
    await test_connection()
    return {"message": "Connection successful"}

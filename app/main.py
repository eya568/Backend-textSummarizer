from math import floor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import message, auth, register, summary



# Directly use os to get the database URL
database_url = "postgresql://postgres:soyed@localhost:5432/postgres"

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
     allow_origins=["*"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(message.router)
app.include_router(auth.router)
app.include_router(register.router)
app.include_router(summary.router)



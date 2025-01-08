from math import floor
import os
import random
import uuid
from app.database import  test_connection

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import message
from app.models import *
import asyncio

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



# Setup the database URI from environment variable (assuming it's set as DATABASE_URL)
db_uri = os.environ['DATABASE_URL'].replace("postgresql://", "cockroachdb://")

# Create a sessionmaker to interact with the database
engine = create_engine(db_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_accounts(session, num):
    """Create N new accounts with random account IDs and account balances."""
    print(f"Creating {num} new accounts...")
    new_accounts = []
    for _ in range(num):
        account_id = uuid.uuid4()
        account_balance = floor(random.random() * 1_000_000)  # Random balance up to 1 million
        new_accounts.append(Account(id=account_id, balance=account_balance))
        print(f"Created new account with id {account_id} and balance {account_balance}.")
    
    session.add_all(new_accounts)
    session.commit()

@app.post("/create-accounts/{num}")
def create_accounts_endpoint(num: int):  # Make this route synchronous
    try:
        # Start a session
        with SessionLocal() as session:
            # Run the transaction to create accounts
            run_transaction(sessionmaker(bind=engine), lambda s: create_accounts(s, num))
        
        return {"message": f"{num} accounts created successfully!"}
    except Exception as e:
        return {"error": str(e)}
def create_summaries(session, num, user_id, content, image):
    """Create N new summaries with random summary IDs, user IDs, content, and images."""
    print("Creating new summaries...")
    new_summaries = []
    seen_summary_ids = []  # Define seen_summary_ids
    while num > 0:
        summary_id = uuid.uuid4()
        new_summaries.append(Summary(id=summary_id, user_id=user_id, content=content, image=image))
        seen_summary_ids.append(summary_id)
        print(f"Created new summary with id {summary_id} for user_id {user_id}.")
        num = num - 1
    session.add_all(new_summaries)
    session.commit()

def get_summaries(session, user_id):
    """Retrieve summaries for a specific user."""
    try:
        summaries = session.query(Summary).filter(Summary.user_id == user_id).all()
        if not summaries:
            print(f"No summaries found for user_id {user_id}.")
        else:
            for summary in summaries:
                print(f"Summary ID: {summary.id}, Content: {summary.content}, Image: {summary.image}, Created At: {summary.created_at}")
        return summaries
    except Exception as e:
        print(f"Error retrieving summaries for user_id {user_id}: {e}")

@app.post("/create-summaries")
async def create_summaries_endpoint(request: Request):
    data = await request.json()
    num = data.get("num")
    user_id = data.get("user_id")
    content = data.get("content")
    image = data.get("image")
    
    try:
        # Run the transaction to create summaries in a separate thread
        await asyncio.to_thread(run_transaction, sessionmaker(bind=engine), lambda s: create_summaries(s, num, user_id, content, image))
        
        return {"message": f"{num} summaries created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summaries/{user_id}")
async def get_summaries_endpoint(user_id: str):
    try:
        # Run the transaction to get summaries in a separate thread
        summaries = await asyncio.to_thread(run_transaction, sessionmaker(bind=engine), lambda s: get_summaries(s, user_id))
        
        return {"summaries": summaries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
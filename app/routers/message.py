from fastapi import APIRouter

router = APIRouter()

@router.get("/message")
async def get_message():
    return {"message": "Hello, this is a simple message!"}

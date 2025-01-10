import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

async def test_asyncpg_connection():
    try:
        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
        print("Connection successful!")
        await conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_asyncpg_connection())

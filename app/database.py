from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, text
from contextlib import asynccontextmanager

# Database URL
DATABASE_URL = "postgresql+asyncpg://aya:JrZOAayLhUvBGlVyAkt06w@text-summarizer8-6889.j77.aws-eu-central-1.cockroachlabs.cloud:26257/defaultdb"

# Create an asynchronous database engine
engine = create_async_engine(DATABASE_URL)
database = engine  # Or you can define another object if needed

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create a metadata instance
metadata = MetaData()

# Dependency to get the database session
@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()  # Rollback in case of error
            raise
        finally:
            await session.close()

async def test_connection():
    try:
        async with engine.connect() as connection:
            # Perform a simple query
            result = await connection.execute(text("SELECT version();"))
            print("Connected to CockroachDB!", result.fetchall())
    except Exception as e:
        print("Error connecting to the database:", e)
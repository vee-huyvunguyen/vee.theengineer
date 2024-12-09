from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData

# FastAPI instance
app = FastAPI()

# Database URL (from .env file or hardcoded for demonstration purposes)
DATABASE_URL = "postgresql://postgres:password@db:5432/mydatabase"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with Postgres!"}

@app.get("/db-status")
async def db_status():
    try:
        with engine.connect() as conn:
            return {"status": "Database connected!"}
    except Exception as e:
        return {"status": f"Database connection failed: {str(e)}"}

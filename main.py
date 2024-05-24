import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from database import Database

# Initialize FastAPI
app = FastAPI()

# Load environment variables
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

engine_args = {
    "pool_size": 20,  # Maximum number of database connections in the pool
    "max_overflow": 50,  # Maximum number of connections that can be created beyond the pool_size
    "pool_timeout": 30,  # Timeout value in seconds for acquiring a connection from the pool
    "pool_recycle": 1800,  # Recycle connections after this number of seconds (optional)
    "pool_pre_ping": False,  # Enable connection health checks (optional)
}

app.add_middleware(DBSessionMiddleware, db_url=DB_URL, engine_args=engine_args)


# Configure CORS middleware
origins = [
    "*",  # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

database = Database(DB_URL)
engine = database.get_engine()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}



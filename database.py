# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Determine the database URL based on an environment variable
TESTING = os.getenv("TESTING", "False") == "True"

if TESTING:
    DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for testing
else:
    # Production database credentials
    DB_USER = os.getenv("POSTGRES_USER", "shopify_user")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "shopify_pass")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "shopify_db")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if TESTING else {}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

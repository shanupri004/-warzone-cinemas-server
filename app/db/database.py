from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# 🔥 THIS LINE FIXES YOUR PROBLEM
from app.models.models import User, Movie, ShowTime, Snack, Booking

def create_db_and_tables():
    print("Tables:", SQLModel.metadata.tables.keys())  # debug
    SQLModel.metadata.create_all(engine)
from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "postgresql://postgres.nrsvriqmngvyhbzjmkmk:WarZone%402026@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# 🔥 THIS LINE FIXES YOUR PROBLEM
from app.models.models import User, Movie, ShowTime, Snack, Booking

def create_db_and_tables():
    print("Tables:", SQLModel.metadata.tables.keys())  # debug
    SQLModel.metadata.create_all(engine)
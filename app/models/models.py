from sqlmodel import SQLModel, Field
from typing import Optional, List
from sqlalchemy import Column, JSON, ForeignKey
from uuid import UUID, uuid4
from datetime import datetime, date, time


# ========================
# USER MODEL (UPDATED UUID)
# ========================
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(nullable=False, unique=True, max_length=255)
    username: str = Field(nullable=False, unique=True, max_length=100)
    password: str = Field(nullable=False)
    role: Optional[str] = Field(default="user", max_length=50)


# ========================
# MOVIE MODEL
# ========================
class Movie(SQLModel, table=True):
    __tablename__ = "movies"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    poster: str
    genre: str
    duration: str
    trailer_url: str
    rating: float
    format: str   # 2D / 3D / IMAX
    description: str
    ticket_price: float


# ========================
# SHOW TIMES
# ========================
class ShowTime(SQLModel, table=True):
    __tablename__ = "show_times"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    movie_id: UUID = Field(
        sa_column=Column(ForeignKey("movies.id", ondelete="CASCADE"))
    )

    show_time: time
    show_date: date

   


# ========================
# SNACKS TABLE
# ========================
class Snack(SQLModel, table=True):
    __tablename__ = "snacks"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    price: float


# ========================
# BOOKING TABLE
# ========================
class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    user_id: UUID = Field(
        sa_column=Column(ForeignKey("users.id"))
    )

    # 🔥 CHANGE HERE
    movie_id: Optional[UUID] = Field(
        default=None,
        sa_column=Column(ForeignKey("movies.id", ondelete="SET NULL"))
    )

    # 🔥 CHANGE HERE
    show_id: Optional[UUID] = Field(
        default=None,
        sa_column=Column(ForeignKey("show_times.id", ondelete="SET NULL"))
    )

    selected_seats: List[str] = Field(sa_column=Column(JSON))

    snacks: List[dict] = Field(
        default=[],
        sa_column=Column(JSON)
    )

    total_amount: float
    transaction_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    

class SnackItem(SQLModel):
    snack_id: UUID
    name: Optional[str]
    quantity: int
    price: Optional[float]
    
class BookingDetails(SQLModel):
    booking_id: UUID
    movie_name: Optional[str]
    poster: Optional[str]
    show_time: Optional[time]
    show_date: Optional[date]
    selected_seats: List[str] 
    snacks: List[SnackItem]
    transaction_id: Optional[str]
    total_amount: float
    

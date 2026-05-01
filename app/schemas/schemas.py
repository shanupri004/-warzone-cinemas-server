from pydantic import BaseModel, EmailStr,field_validator
from typing import Optional
from typing import List
from datetime import date, time
from enum import Enum
from uuid import UUID


class CastEntry(BaseModel):
    role: Optional[str] = "user"
    actor_name: str
    character_name: str
    image: str

# Register input schema
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: str = "user"

# Login input schema
class UserLogin(BaseModel):
    username: str
    password: str
    
class CastUpdateRequest(BaseModel):
    castList: List[CastEntry]

class PaymentStatus(str, Enum):
    cancel = "cancel"
    pending = "pending"
    complete = "complete"

class BookingBase(BaseModel):
    user_id: int
    user_name: str
    movie_id: int   
    movie_name: str
    date: date
    time: str
    screen: str
    selected_seats: str
    snacks: float = 0
    delivery: bool = False
    ticket_price: float
    total: float
    is_paid: PaymentStatus = PaymentStatus.pending

class BookingCreate(BookingBase):
    pass

class BookingRead(BookingBase):
    id: int
    booking_id: str

    model_config = {
        "from_attributes": True
    }

class ReviewCreate(BaseModel):
    user_id: int
    user_name: str
    movie_id: int
    rating: float   # match DECIMAL(2,1)
    comment: str


class ReviewRead(BaseModel):
    review_id: int
    user_id: int
    user_name: str
    movie_id: int
    rating: float
    comment: str

    model_config = {"from_attributes": True}

class ShowTimeCreate(BaseModel):
    movie_id: UUID
    show_date: date
    show_time: time

    @field_validator('movie_id', mode='before')
    @classmethod
    def convert_movie_id(cls, v):
        if isinstance(v, str):
            return UUID(v)
        return v
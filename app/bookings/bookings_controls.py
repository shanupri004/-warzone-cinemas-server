from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from app.db.database import get_session
from app.models.models import Booking, BookingDetails, Movie, ShowTime, Snack, SnackItem

router = APIRouter()


# =========================
# GET ALL BOOKINGS
# =========================
@router.get("/", response_model=List[Booking])
def get_bookings(session: Session = Depends(get_session)):
    return session.exec(select(Booking)).all()


# =========================
# GET BOOKING BY ID
# =========================
@router.get("/{id}", response_model=Booking)
def get_booking(id: UUID, session: Session = Depends(get_session)):
    booking = session.get(Booking, id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking


# =========================
# GET BOOKINGS BY USER ID
# =========================
@router.get("/user/{user_id}", response_model=List[BookingDetails])
def get_bookings_by_user(user_id: UUID, session: Session = Depends(get_session)):

    stmt = (
        select(
            Booking.id,
            Movie.name,
            Movie.poster,
            ShowTime.show_time,
            ShowTime.show_date,
            Booking.selected_seats,
            Booking.snacks,
            Booking.transaction_id,
            Booking.total_amount
        )
        .join(Movie, Movie.id == Booking.movie_id, isouter=True)
        .join(ShowTime, ShowTime.id == Booking.show_id, isouter=True)
        .where(Booking.user_id == user_id)
    )

    rows = session.exec(stmt).all()

    # 🔹 Step 1: Collect all snack_ids
    all_snack_ids = set()

    for row in rows:
        raw_snacks = row[6] or []
        for item in raw_snacks:
            if "snack_id" in item:
                all_snack_ids.add(item["snack_id"])

    # 🔹 Step 2: Fetch all snacks in ONE query
    snacks_db = session.exec(
        select(Snack).where(Snack.id.in_(all_snack_ids))
    ).all()

    snack_map = {
        str(s.id): {"name": s.name, "price": s.price}
        for s in snacks_db
    }

    results = []

    # 🔹 Step 3: Build response
    for row in rows:
        raw_snacks = row[6] or []

        enriched_snacks = [
            SnackItem(
                snack_id=item.get("snack_id"),
                name=snack_map.get(item.get("snack_id"), {}).get("name"),
                quantity=item.get("quantity"),
                price=snack_map.get(item.get("snack_id"), {}).get("price"),
            )
            for item in raw_snacks
        ]

        results.append(
            BookingDetails(
                booking_id=row[0],
                movie_name=row[1],
                poster=row[2],
                show_time=row[3],
                show_date=row[4],
                selected_seats=row[5] or [],
                snacks=enriched_snacks,
                transaction_id=row[7],
                total_amount=row[8],
            )
        )

    return results

# =========================
# GET BOOKINGS BY MOVIE ID
# =========================
@router.get("/movie/{movie_id}", response_model=List[Booking])
def get_bookings_by_movie(movie_id: UUID, session: Session = Depends(get_session)):
    bookings = session.exec(select(Booking).where(Booking.movie_id == movie_id)).all()
    return bookings


# =========================
# CREATE BOOKING
# =========================
@router.post("/", response_model=Booking)
def create_booking(booking: Booking, session: Session = Depends(get_session)):
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking


# =========================
# UPDATE BOOKING
# =========================
# @router.put("/{id}", response_model=Booking)
# def update_booking(id: UUID, booking: Booking, session: Session = Depends(get_session)):
#     db_booking = session.get(Booking, id)

#     if not db_booking:
#         raise HTTPException(404, "Booking not found")

#     booking_data = booking.dict(exclude_unset=True)

#     for key, value in booking_data.items():
#         setattr(db_booking, key, value)

#     session.add(db_booking)
#     session.commit()
#     session.refresh(db_booking)

#     return db_booking


# =========================
# DELETE BOOKING
# =========================
@router.delete("/{id}")
def delete_booking(id: UUID, session: Session = Depends(get_session)):
    booking = session.get(Booking, id)

    if not booking:
        raise HTTPException(404, "Booking not found")

    session.delete(booking)
    session.commit()

    return {"message": "Booking deleted"}

# =========================
# GET BOOKINGS BY SHOW ID
# =========================
@router.get("/show/{show_id}", response_model=List[Booking])
def get_bookings_by_show(show_id: UUID, session: Session = Depends(get_session)):
    bookings = session.exec(
        select(Booking).where(Booking.show_id == show_id)
    ).all()

    return bookings

# =========================
# GET BOOKED SEATS BY SHOW
# =========================
@router.get("/show/{show_id}/seats", response_model=List[str])
def get_booked_seats(show_id: UUID, session: Session = Depends(get_session)):
    bookings = session.exec(
        select(Booking.selected_seats).where(Booking.show_id == show_id)
    ).all()

    # flatten list
    seats = [seat for sublist in bookings for seat in sublist]

    return seats
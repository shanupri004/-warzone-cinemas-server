from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from pydantic import BaseModel
from uuid import UUID

from app.db.database import get_session
from app.models.models import ShowTime, Movie
from app.schemas.schemas import ShowTimeCreate

router = APIRouter()


# =========================
# GET ALL SHOWTIMES
# =========================
@router.get("/", response_model=List[ShowTime])
def get_showtimes(session: Session = Depends(get_session)):
    return session.exec(select(ShowTime)).all()


# =========================
# GET SHOWTIMES BY MOVIE
# =========================
@router.get("/movie/{movie_id}", response_model=List[ShowTime])
def get_showtimes_by_movie(movie_id: UUID, session: Session = Depends(get_session)):
    showtimes = session.exec(
        select(ShowTime).where(ShowTime.movie_id == movie_id)
    ).all()

    return showtimes


# =========================
# GET BY ID
# =========================
@router.get("/{id}", response_model=ShowTime)
def get_showtime(id: UUID, session: Session = Depends(get_session)):
    showtime = session.get(ShowTime, id)

    if not showtime:
        raise HTTPException(404, "ShowTime not found")

    return showtime


# =========================
# CREATE SHOWTIME
# =========================
@router.post("/", response_model=ShowTime)
def create_showtime(data: ShowTimeCreate, session: Session = Depends(get_session)):
    
    # validate movie
    movie = session.get(Movie, data.movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    # create DB object
    showtime = ShowTime(**data.dict())

    session.add(showtime)
    session.commit()
    session.refresh(showtime)

    return showtime


# =========================
# UPDATE SHOWTIME
# =========================
@router.put("/{id}", response_model=ShowTime)
def update_showtime(id: UUID, showtime: ShowTime, session: Session = Depends(get_session)):
    db_showtime = session.get(ShowTime, id)

    if not db_showtime:
        raise HTTPException(404, "ShowTime not found")

    update_data = showtime.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_showtime, key, value)

    session.add(db_showtime)
    session.commit()
    session.refresh(db_showtime)

    return db_showtime


# =========================
# DELETE SHOWTIME
# =========================
@router.delete("/{id}")
def delete_showtime(id: UUID, session: Session = Depends(get_session)):
    showtime = session.get(ShowTime, id)

    if not showtime:
        raise HTTPException(404, "ShowTime not found")

    session.delete(showtime)
    session.commit()

    return {"message": "ShowTime deleted"}


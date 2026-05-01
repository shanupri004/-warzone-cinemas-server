from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from app.db.database import get_session
from app.models.models import Movie

router = APIRouter()


# =========================
# GET ALL MOVIES
# =========================
@router.get("/", response_model=List[Movie])
def get_movies(session: Session = Depends(get_session)):
    return session.exec(select(Movie)).all()


# =========================
# GET BY ID
# =========================
@router.get("/{id}", response_model=Movie)
def get_movie(id: UUID, session: Session = Depends(get_session)):
    movie = session.get(Movie, id)
    if not movie:
        raise HTTPException(404, "Movie not found")
    return movie
    

# =========================
# CREATE
# =========================
@router.post("/", response_model=Movie)
def create_movie(movie: Movie, session: Session = Depends(get_session)):
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


# =========================
# UPDATE
# =========================
@router.put("/{id}", response_model=Movie)
def update_movie(id: UUID, movie: Movie, session: Session = Depends(get_session)):
    db_movie = session.get(Movie, id)

    if not db_movie:
        raise HTTPException(404, "Movie not found")

    movie_data = movie.dict(exclude_unset=True)

    for key, value in movie_data.items():
        setattr(db_movie, key, value)

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)

    return db_movie


# =========================
# DELETE (REAL DELETE)
# =========================
@router.delete("/{id}")
def delete_movie(id: UUID, session: Session = Depends(get_session)):
    movie = session.get(Movie, id)

    if not movie:
        raise HTTPException(404, "Movie not found")

    session.delete(movie)
    session.commit()

    return {"message": "Movie deleted"}
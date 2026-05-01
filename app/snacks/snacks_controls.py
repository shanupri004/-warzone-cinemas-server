from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from app.db.database import get_session
from app.models.models import Snack

router = APIRouter()


# =========================
# GET ALL SNACKS
# =========================
@router.get("/", response_model=List[Snack])
def get_snacks(session: Session = Depends(get_session)):
    return session.exec(select(Snack)).all()


# =========================
# GET SNACK BY ID
# =========================
@router.get("/{id}", response_model=Snack)
def get_snack(id: UUID, session: Session = Depends(get_session)):
    snack = session.get(Snack, id)
    if not snack:
        raise HTTPException(404, "Snack not found")
    return snack


# =========================
# CREATE SNACK
# =========================
@router.post("/", response_model=Snack)
def create_snack(snack: Snack, session: Session = Depends(get_session)):
    session.add(snack)
    session.commit()
    session.refresh(snack)
    return snack


# =========================
# UPDATE SNACK
# =========================
@router.put("/{id}", response_model=Snack)
def update_snack(id: UUID, snack: Snack, session: Session = Depends(get_session)):
    db_snack = session.get(Snack, id)

    if not db_snack:
        raise HTTPException(404, "Snack not found")

    snack_data = snack.dict(exclude_unset=True)

    for key, value in snack_data.items():
        setattr(db_snack, key, value)

    session.add(db_snack)
    session.commit()
    session.refresh(db_snack)

    return db_snack


# =========================
# DELETE SNACK
# =========================
@router.delete("/{id}")
def delete_snack(id: UUID, session: Session = Depends(get_session)):
    snack = session.get(Snack, id)

    if not snack:
        raise HTTPException(404, "Snack not found")

    session.delete(snack)
    session.commit()

    return {"message": "Snack deleted"}

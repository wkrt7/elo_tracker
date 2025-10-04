from typing import List

from auth.security import get_current_active_user
from config import K_FACTOR_LONG, K_FACTOR_SHORT, get_db
from crud.match import match_crud
from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError
from schemas.match import MatchCreate, MatchInternal, MatchRead
from services.elo_service import EloService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/matches", tags=["matches"], dependencies=[Depends(get_current_active_user)])


@router.post("/add_match/", response_model=MatchRead)
def add_match(match: MatchCreate, db: Session = Depends(get_db)):
    elo_service = EloService(db)
    try:
        k_factor = K_FACTOR_LONG if match.is_long else K_FACTOR_SHORT
        match_internal = MatchInternal(**match.model_dump(), k_factor=k_factor)
        participants = elo_service.calculate_and_update(match_internal)
        match_internal.participants = participants
        db_match = match_crud.create(db, match_internal)
        db.commit()
        db.refresh(db_match)
        return db_match
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Transaction failed {e}")
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Transaction failed: {e}")


@router.get("/get_match/", response_model=MatchRead)
def get_match(id: int, db: Session = Depends(get_db)):
    match = match_crud.get(db, id=id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.get("/get_matches/", response_model=List[MatchRead])
def get_matches(db: Session = Depends(get_db)):
    match = match_crud.get_all(db)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

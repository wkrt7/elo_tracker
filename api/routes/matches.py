from typing import List

from auth.security import get_current_active_user
from config import get_db
from crud.match import match_crud
from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError
from schemas.match import MatchCreate, MatchRead
from services.elo_service import EloService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/matches", tags=["matches"], dependencies=[Depends(get_current_active_user)])


@router.post("/add_match/", response_model=MatchRead)
def add_match(match: MatchCreate, db: Session = Depends(get_db)):
    elo_service = EloService(db)
    try:

        participants = elo_service.calculate_and_update(match)
        match_data = match.model_copy(update={"participants": participants})
        db_match = match_crud.create(db, match_data)
        db.commit()
        db.refresh(db_match)
        return db_match
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Transaction failed {e}")


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

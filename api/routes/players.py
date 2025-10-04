from typing import List

from auth.security import get_current_active_user
from config import get_db
from crud.player import player_crud
from fastapi import APIRouter, Depends, HTTPException
from schemas.player import PlayerCreate, PlayerRead
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/players", tags=["players"], dependencies=[Depends(get_current_active_user)]
)


@router.post("/", response_model=PlayerRead)
def create_player(player_in: PlayerCreate, db: Session = Depends(get_db)):
    try:
        player = player_crud.create(db, player_in)
        db.commit()
        return player
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=PlayerRead)
def read_player(
    id: int | None = None, name: str | None = None, db: Session = Depends(get_db)
):
    if id:
        ret = player_crud.get(db, id=id)
    elif name:
        ret = player_crud.get_player_by_name(db, name=name)
    if ret:
        return ret
    raise HTTPException(status_code=404, detail="Player not found")


@router.get("/get_players/", response_model=List[PlayerRead])
def get_players(db: Session = Depends(get_db)):
    ret = player_crud.get_all(db=db)
    if not ret:
        raise HTTPException(status_code=404, detail="No players found")
    return ret

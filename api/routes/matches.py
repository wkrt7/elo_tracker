from typing import List

from auth.security import get_current_active_user
from config import get_db
from crud.match import match_crud, match_participant_crud
from crud.player import player_crud
from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError
from schemas.match import MatchCreate, MatchParticipantCreate, MatchRead
from schemas.player import PlayerCreate, PlayerRead, PlayerUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/matches", tags=["matches"], dependencies=[Depends(get_current_active_user)])


@router.post("/add_match/", response_model=MatchRead)
def add_match(match: MatchCreate, db: Session = Depends(get_db)):

    try:
        player_ids = [p.player_id for p in match.participants]
        players = {p.id: p for p in player_crud.batch_get(db, player_ids, with_transaction=True)}

        team_a = [players[p.player_id] for p in match.participants if p.team_side == 1]
        team_b = [players[p.player_id] for p in match.participants if p.team_side == 2]

        avg_elo_a = sum(p.elo for p in team_a) / len(team_a)
        avg_elo_b = sum(p.elo for p in team_b) / len(team_b)
        # Prepare participant dicts with elo_before / elo_after
        participants = []
        for p in match.participants:
            player = players[p.player_id]
            part_dict = p.model_dump()
            part_dict["elo_before"] = player.elo
            if p.team_side == 1:
                expected = 1 / (1 + 10 ** ((avg_elo_b - player.elo) / 400))
                score = 1 if match.winner_team_side == 1 else 0
            else:
                expected = 1 / (1 + 10 ** ((avg_elo_a - player.elo) / 400))
                score = 1 if match.winner_team_side == 2 else 0

            new_elo = player.elo + match.k_factor * (score - expected)
            part_dict["elo_after"] = new_elo
            print(new_elo)
            participants.append(part_dict)
            player_crud.update(db=db, id=p.player_id, obj_in=PlayerUpdate(elo=part_dict["elo_after"]))

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

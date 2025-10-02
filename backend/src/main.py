import os
from typing import List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from psycopg2 import IntegrityError
from pydantic import BaseModel, ValidationError
from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, text
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker
from src.models import Team, TeamParticipant

from backend.src.schemas.match import MatchCreate, MatchParticipantCreate, MatchRead
from backend.src.schemas.player import PlayerCreate, PlayerRead, PlayerUpdate

from .crud.match import match_crud, match_participant_crud
from .crud.player import player_crud
from .crud.team import team_crud, team_participant_crud
from .models.player import Player
from .schemas.team import TeamCreate, TeamParticipantCreate, TeamRead

load_dotenv()  # loads .env into environment variables

DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_ID = os.environ["DB_ID"]

connection_string = (
    f"postgresql://postgres.vkqxkuvqhzlsocnncoik:{DB_PASSWORD}@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
)
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


# --- DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/players/", response_model=PlayerRead)
def create_player(player_in: PlayerCreate, db: Session = Depends(get_db)):
    try:
        p = player_crud.create(db, player_in)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Transaction failed {e}")
        return p
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/players/", response_model=PlayerRead)
def read_player(id: int | None = None, name: str | None = None, db: Session = Depends(get_db)):
    if id:
        return player_crud.get(db, id=id)
    elif name:
        return player_crud.get_player_by_name(db, name=name)


@app.post("/team/", response_model=TeamRead)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    try:
        team_db = team_crud.create(db, team)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Transaction failed {e}")
        return team_db
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_teams/", response_model=List[TeamRead])
def get_teams(db: Session = Depends(get_db)):
    teams = team_crud.get_all(db)
    return teams


@app.post("/team_participant/", response_model=TeamParticipantCreate)
def create_team_participant(tp: TeamParticipantCreate, db: Session = Depends(get_db)):
    try:
        tp_db = team_participant_crud.create(db, tp)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Transaction failed {e}")
        return tp_db
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/team_with_player/", response_model=TeamRead)
def create_team_with_players(team: TeamCreate, player_names: list[str], db: Session = Depends(get_db)):
    try:
        players = player_crud.batch_get_by_names(names=player_names, db=db, with_transaction=True)

        team_db = team_crud.create(db, team)
        for player in players:
            _ = team_participant_crud.create(
                db=db, obj_in=TeamParticipantCreate(team_id=team_db.id, player_id=player.id)
            )

        db.commit()
        db.refresh(team_db)  # make sure all relationships are loaded
        return team_db
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_match/", response_model=MatchRead)
def add_match(match: MatchCreate, db: Session = Depends(get_db)):
    db_match = match_crud.create(db, match)

    participants = db_match.team_a.participants + db_match.team_b.participants
    mps = []
    for par in participants:
        player: Player = player_crud.get(db, par.player_id, with_transaction=True)
        mp = match_participant_crud.create(
            db,
            obj_in=MatchParticipantCreate(
                match_id=db_match.id,
                player_id=par.player_id,
                team_id=par.team_id,
                elo_before=player.elo,
                elo_after=player.elo + 1,
            ),
        )
        player_crud.update(db, player.id, obj_in=PlayerUpdate(name=player.name, elo=mp.elo_after))
    try:
        db.commit()
        db.refresh(db_match)
        return db_match
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Transaction failed {e}")

# import os
# from typing import List

# from dotenv import load_dotenv
# from fastapi import Depends, FastAPI, HTTPException
# from psycopg2 import IntegrityError
# from pydantic import BaseModel, ValidationError
# from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, text
# from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

# from .crud.match import match_crud, match_participant_crud
# from .crud.player import player_crud
# from .models.player import Player
# from .schemas.match import MatchCreate, MatchParticipantCreate, MatchRead
# from .schemas.player import PlayerCreate, PlayerRead, PlayerUpdate

# load_dotenv()  # loads .env into environment variables

# DB_PASSWORD = os.environ["DB_PASSWORD"]
# DB_ID = os.environ["DB_ID"]
# DB_URL = os.environ["DB_URL"]
# DB_PORT = os.environ.get("DB_PORT")

# connection_string = f"postgresql://postgres.{DB_ID}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/postgres"

# engine = create_engine(connection_string)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()


# # --- DEPENDENCY ---
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI on Vercel!"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# @app.post("/players/", response_model=PlayerRead)
# def create_player(player_in: PlayerCreate, db: Session = Depends(get_db)):
#     try:
#         p = player_crud.create(db, player_in)
#         try:
#             db.commit()
#         except IntegrityError as e:
#             db.rollback()
#             raise HTTPException(status_code=400, detail="Transaction  failed {e}")
#         return p
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @app.get("/players/", response_model=PlayerRead)
# def read_player(id: int | None = None, name: str | None = None, db: Session = Depends(get_db)):
#     if id:
#         return player_crud.get(db, id=id)
#     elif name:
#         return player_crud.get_player_by_name(db, name=name)


# @app.post("/add_match/", response_model=MatchRead)
# def add_match(match: MatchCreate, db: Session = Depends(get_db)):
#     player_ids = [p.player_id for p in match.participants]
#     players = {p.id: p for p in player_crud.batch_get(db, player_ids, with_transaction=True)}

#     team_a = [players[p.player_id] for p in match.participants if p.team_side == 1]
#     team_b = [players[p.player_id] for p in match.participants if p.team_side == 2]

#     avg_elo_a = sum(p.elo for p in team_a) / len(team_a)
#     avg_elo_b = sum(p.elo for p in team_b) / len(team_b)
#     # Prepare participant dicts with elo_before / elo_after
#     participants = []
#     for p in match.participants:
#         player = players[p.player_id]
#         part_dict = p.model_dump()
#         part_dict["elo_before"] = player.elo
#         if p.team_side == 1:
#             expected = 1 / (1 + 10 ** ((avg_elo_b - player.elo) / 400))
#             score = 1 if match.winner_team_side == 1 else 0
#         else:
#             expected = 1 / (1 + 10 ** ((avg_elo_a - player.elo) / 400))
#             score = 1 if match.winner_team_side == 2 else 0

#         new_elo = player.elo + match.k_factor * (score - expected)
#         part_dict["elo_after"] = new_elo
#         print(new_elo)
#         participants.append(part_dict)
#         player_crud.update(db=db, id=p.player_id, obj_in=PlayerUpdate(elo=part_dict["elo_after"]))

#     match_data = match.model_copy(update={"participants": participants})
#     db_match = match_crud.create(db, match_data)

#     try:
#         db.commit()
#         db.refresh(db_match)
#         return db_match
#     except IntegrityError as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="Transaction failed {e}")


# @app.get("/get_match/", response_model=MatchRead)
# def get_match(id: int, db: Session = Depends(get_db)):
#     match = match_crud.get(db, id=id)
#     if not match:
#         raise HTTPException(status_code=404, detail="Match not found")
#     return match


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)

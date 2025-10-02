import os

from dotenv import load_dotenv
from models.player import Player
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker


def create_player(db: Session, player: PlayerCreate):
    db_player = Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def bulk_insert_players(db: Session, players: list[PlayerCreate]):
    db.bulk_insert_mappings(Player, [p.model_dump() for p in players])
    db.commit()


def get_player(db: Session, player_id: int) -> Player:
    return db.query(Player).filter(Player.player_id == player_id).first()


def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Player).offset(skip).limit(limit).all()


load_dotenv()  # loads .env into environment variables

DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_ID = os.environ["DB_ID"]

connection_string = (
    f"postgresql://postgres.vkqxkuvqhzlsocnncoik:{DB_PASSWORD}@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
)
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

new_player = create_player(db, PlayerCreate(user_name="Alice", elo=1200))
print(new_player.player_id, new_player.user_name)
print(get_player(db, 1).user_name)
ret = get_player(db, 1)
player_read = PlayerRead.model_validate(ret)
print(player_read.model_dump())

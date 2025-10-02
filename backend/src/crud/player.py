from typing import List, Optional

from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from src.models import Player
from src.schemas.player import PlayerCreate


def get_player(db: Session, player_id: int) -> Optional[Player]:
    return db.query(Player).filter(Player.id == player_id).first()


def get_player_by_name(db: Session, name: str) -> Optional[Player]:
    """
    Fetch a single player by their username (name).
    Returns None if not found.
    """
    return db.query(Player).filter(Player.name == name).first()


def get_players(db: Session, skip: int = 0, limit: int = 100) -> List[Player]:
    return db.query(Player).offset(skip).limit(limit).all()


def create_player(db: Session, player: PlayerCreate) -> Player:
    db_player = Player(name=player.name)
    db.add(db_player)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Player with name '{player.name}' already exists")
    db.refresh(db_player)
    return db_player


def update_player(db: Session, player_id: int, data) -> Player:
    raise NotImplementedError("Update operation is not implemented yet")


def delete_player(db: Session, player_id: int) -> Optional[Player]:
    db_player = get_player(db, player_id)
    if not db_player:
        return None
    db.delete(db_player)
    db.commit()
    return db_player

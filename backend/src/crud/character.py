from typing import List, Optional

from sqlalchemy.orm import Session
from src.models import Character
from src.schemas.character import CharacterCreate


def get_character(db: Session, character_id: int) -> Optional[Character]:
    return db.query(Character).filter(Character.id == character_id).first()


def get_characters(db: Session, skip: int = 0, limit: int = 100) -> List[Character]:
    return db.query(Character).offset(skip).limit(limit).all()


def create_character(db: Session, character: CharacterCreate) -> Character:
    db_character = Character(name=character.name)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character


def delete_character(db: Session, character_id: int) -> Optional[Character]:
    db_character = get_character(db, character_id)
    if not db_character:
        return None
    db.delete(db_character)
    db.commit()
    return db_character


def update_character(db: Session, character_id: int, data) -> Character:
    raise NotImplementedError("Update operation is not implemented yet")

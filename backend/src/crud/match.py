from typing import List, Optional

from sqlalchemy.orm import Session
from src.models import Match, MatchParticipant
from src.schemas.match import MatchCreate, MatchParticipantCreate


def get_match(db: Session, match_id: int) -> Optional[Match]:
    return db.query(Match).filter(Match.id == match_id).first()


def get_matches(db: Session, skip: int = 0, limit: int = 100) -> List[Match]:
    return db.query(Match).offset(skip).limit(limit).all()


def create_match(db: Session, match: MatchCreate) -> Match:
    db_match = Match(
        team_a_id=match.team_a_id,
        team_b_id=match.team_b_id,
        team_size=match.team_size,
        k_factor=match.k_factor,
        description=match.description,
        finish_type_id=match.finish_type_id,
        is_long=match.is_long,
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def add_match_participant(db: Session, participant: MatchParticipantCreate) -> MatchParticipant:
    db_participant = MatchParticipant(
        match_id=participant.match_id,
        player_id=participant.player_id,
        team_id=participant.team_id,
        character_id=participant.character_id,
        elo_before=participant.elo_before,
        elo_after=participant.elo_after,
    )
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant


def update_match(db: Session, match_id: int, data) -> Match:
    raise NotImplementedError("Update operation is not implemented yet")

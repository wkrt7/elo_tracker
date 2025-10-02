from typing import List, Optional

from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from src.models import Team, TeamParticipant
from src.schemas.team import TeamCreate, TeamParticipantCreate

from backend.src.models.player import Player


def get_team(db: Session, team_id: int) -> Optional[Team]:
    return db.query(Team).filter(Team.id == team_id).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100) -> List[Team]:
    return db.query(Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: TeamCreate) -> Team:
    db_team = Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def add_team_participant(db: Session, participant: TeamParticipantCreate) -> TeamParticipant:
    player = db.query(Player).filter(Player.id == participant.player_id).first()
    if not player:
        raise ValueError(f"Player with id {participant.player_id} does not exist.")

    # Add the team participant
    try:
        db_participant = TeamParticipant(team_id=participant.team_id, player_id=participant.player_id)
        db.add(db_participant)
        db.commit()
        db.refresh(db_participant)
        return db_participant
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Failed to add participant. Ensure the team and player combination is unique.") from e


def update_team(db: Session, team_id: int, data) -> Team:
    raise NotImplementedError("Update operation is not implemented yet")

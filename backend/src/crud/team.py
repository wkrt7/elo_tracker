from typing import List, Optional

from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from src.models import Team, TeamParticipant
from src.schemas.team import TeamCreate, TeamParticipantCreate

from backend.src.crud.base import CRUDBase
from backend.src.models.player import Player


class TeamParticipantCRUD(CRUDBase[TeamParticipant, TeamParticipantCreate]):
    def __init__(self):
        super().__init__(TeamParticipant)

    def pre_create(self, db: Session, obj_in: TeamParticipantCreate):
        # Check if player exists
        if db.query(Player).filter(Player.id == obj_in.player_id).first() is None:
            raise ValueError(f"Player with id {obj_in.player_id} does not exist")
        return obj_in

    def create(self, db: Session, obj_in: TeamParticipantCreate) -> TeamParticipant:
        obj_in = self.pre_create(db, obj_in)
        db_participant = TeamParticipant(team_id=obj_in.team_id, player_id=obj_in.player_id)
        db.add(db_participant)
        db.flush()
        return db_participant


team_crud = CRUDBase[Team, TeamCreate](Team)
team_participant_crud = TeamParticipantCRUD()

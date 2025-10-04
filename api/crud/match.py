from crud.base import CRUDBase
from models import Match, MatchParticipant
from schemas.match import (
    MatchCreate,
    MatchParticipantCreate,
    MatchParticipantUpdate,
    MatchUpdate,
)
from sqlalchemy.orm import Session


class MatchCrud(CRUDBase[Match, MatchCreate, MatchUpdate]):
    def create(self, db: Session, obj_in: MatchCreate) -> Match:
        obj_data = obj_in.model_dump()

        # Special handling for relationships
        if "participants" in obj_data:
            participants_data = obj_data.pop("participants")
        else:
            participants_data = []

        db_obj = self.model(**obj_data)

        # Convert participants into ORM objects
        for part in participants_data:
            print(part)
            db_obj.participants.append(MatchParticipant(**part))

        db.add(db_obj)
        db.flush()
        return db_obj


match_crud = MatchCrud(Match)
match_participant_crud = CRUDBase[MatchParticipant, MatchParticipantCreate, MatchParticipantUpdate](MatchParticipant)

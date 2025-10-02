from typing import List, Optional

from sqlalchemy.orm import Session
from src.models import Match, MatchParticipant
from src.schemas.match import (
    MatchCreate,
    MatchParticipantCreate,
    MatchParticipantUpdate,
    MatchUpdate,
)

from backend.src.crud.base import CRUDBase

match_crud = CRUDBase[Match, MatchCreate, MatchUpdate](Match)
match_participant_crud = CRUDBase[MatchParticipant, MatchParticipantCreate, MatchParticipantUpdate](MatchParticipant)

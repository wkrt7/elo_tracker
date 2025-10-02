from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .team import TeamRead


class MatchBase(BaseModel):
    description: Optional[str] = None
    is_long: bool = False
    team_size: int
    k_factor: float
    winner_team_id: int


class MatchCreate(MatchBase):
    team_a_id: int
    team_b_id: int


class MatchRead(MatchBase):
    id: int
    date: datetime
    team_a: TeamRead
    team_b: TeamRead
    participants: List["MatchParticipantRead"]
    model_config = ConfigDict(from_attributes=True)


class MatchParticipantCreate(BaseModel):
    match_id: int
    player_id: int
    team_id: int
    character_id: Optional[int] = None
    elo_before: float
    elo_after: float


class MatchParticipantRead(BaseModel):
    id: int
    match_id: int
    player_id: int
    team_id: int
    character_id: Optional[int] = None
    elo_before: float
    elo_after: float

    model_config = ConfigDict(from_attributes=True)

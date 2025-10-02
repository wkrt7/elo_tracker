from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .player import PlayerRead


class TeamBase(BaseModel):
    name: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int
    participants: List[PlayerRead] = []

    model_config = ConfigDict(from_attributes=True)


class TeamParticipantCreate(BaseModel):
    team_id: int
    player_id: int


class TeamParticipantRead(BaseModel):
    id: int
    team_id: int
    player_id: int

    model_config = ConfigDict(from_attributes=True)

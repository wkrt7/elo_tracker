from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class MatchBase(BaseModel):
    description: Optional[str] = None
    finish_type_id: Optional[int] = None
    is_long: bool = True
    team_size: int
    k_factor: float
    winner_team_side: Optional[int] = None  # 1, 2, or None
    participants: List["MatchParticipantCreate"]

    @field_validator("team_size")
    def validate_team_size(cls, v):
        if v not in [1, 2, 3, 4, 5]:
            raise ValueError("Team size must be 1-5")
        return v

    @field_validator("winner_team_side")
    def validate_winner_side(cls, v):
        if v is not None and v not in [1, 2]:
            raise ValueError("Winner team side must be 1 or 2")
        return v


class MatchCreate(MatchBase):
    pass


class MatchRead(MatchBase):
    id: int
    date: datetime
    model_config = ConfigDict(from_attributes=True)


class MatchUpdate(BaseModel):
    description: Optional[str] = None
    finish_type_id: Optional[int] = None
    winner_team_side: Optional[int] = None

    @field_validator("winner_team_side")
    def validate_winner_side(cls, v):
        if v is not None and v not in [1, 2]:
            raise ValueError("Winner team side must be 1 or 2")
        return v


class MatchParticipantBase(BaseModel):
    pass


class MatchParticipantCreate(MatchParticipantBase):
    player_id: int
    team_side: int  # 1 or 2
    character_id: Optional[int] = None

    @field_validator("team_side")
    def validate_team_side(cls, v):
        if v not in [1, 2]:
            raise ValueError("Team side must be 1 or 2")
        return v


class MatchParticipantRead(MatchParticipantBase):
    id: int
    match_id: int
    player_id: int
    team_side: int
    character_id: Optional[int] = None
    elo_before: float
    elo_after: float

    model_config = ConfigDict(from_attributes=True)


class MatchParticipantUpdate(BaseModel):
    character_id: Optional[int] = None
    team_side: Optional[int] = None

    @field_validator("team_side")
    def validate_team_side(cls, v):
        if v is not None and v not in [1, 2]:
            raise ValueError("Team side must be 1 or 2")
        return v

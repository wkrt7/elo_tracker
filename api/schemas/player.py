from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator, validator


class PlayerBase(BaseModel):
    name: str

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Player name cannot be empty")
        return v


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    elo: float


class PlayerRead(PlayerBase):
    id: int
    elo: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

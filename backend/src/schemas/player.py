from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class PlayerRead(PlayerBase):
    id: int
    elo: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

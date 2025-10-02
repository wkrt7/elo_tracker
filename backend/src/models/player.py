import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    elo: Mapped[float] = mapped_column(Float, default=1000.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))

    team_participations: Mapped[list["TeamParticipant"]] = relationship(back_populates="player")
    match_participations: Mapped[list["MatchParticipant"]] = relationship(back_populates="player")

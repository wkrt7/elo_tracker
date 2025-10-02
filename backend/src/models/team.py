from typing import Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    participants: Mapped[list["TeamParticipant"]] = relationship(back_populates="team")
    matches_as_team_a: Mapped[list["Match"]] = relationship(foreign_keys="Match.team_a_id", back_populates="team_a")
    matches_as_team_b: Mapped[list["Match"]] = relationship(foreign_keys="Match.team_b_id", back_populates="team_b")
    matches_won: Mapped[list["Match"]] = relationship(foreign_keys="Match.winner_team_id", back_populates="winner_team")


class TeamParticipant(Base):
    __tablename__ = "team_participant"
    __table_args__ = (
        # unique constraint
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))

    team: Mapped["Team"] = relationship(back_populates="participants")
    player: Mapped["Player"] = relationship(back_populates="team_participations")

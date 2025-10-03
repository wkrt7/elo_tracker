import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Match(Base):
    __tablename__ = "match"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    finish_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("finish_type.id"), nullable=True)
    is_long: Mapped[bool] = mapped_column(Boolean, default=False)
    team_size: Mapped[int] = mapped_column(Integer)
    k_factor: Mapped[float] = mapped_column(Float)
    # team_a_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    # team_b_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    winner_team_side: Mapped[Optional[int]] = mapped_column(nullable=False)

    finish_type: Mapped[Optional["FinishType"]] = relationship(back_populates="matches")
    # team_a: Mapped["Team"] = relationship(foreign_keys=[team_a_id], back_populates="matches_as_team_a")
    # team_b: Mapped["Team"] = relationship(foreign_keys=[team_b_id], back_populates="matches_as_team_b")
    # winner_team: Mapped[Optional["Team"]] = relationship(foreign_keys=[winner_team_id], back_populates="matches_won")
    participants: Mapped[list["MatchParticipant"]] = relationship(back_populates="match")


class MatchParticipant(Base):
    __tablename__ = "match_participant"
    __table_args__ = (UniqueConstraint("match_id", "player_id", name="uq_match_player"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("match.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("character.id"), nullable=True)
    elo_before: Mapped[float] = mapped_column(Float)
    elo_after: Mapped[float] = mapped_column(Float)
    team_side: Mapped[int] = mapped_column(nullable=False)

    match: Mapped["Match"] = relationship(back_populates="participants")
    player: Mapped["Player"] = relationship(back_populates="match_participations")
    character: Mapped[Optional["Character"]] = relationship(back_populates="match_participations")
    # team: Mapped["Team"] = relationship()

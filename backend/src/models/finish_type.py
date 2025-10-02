from datetime import datetime
from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base


class FinishType(Base):
    __tablename__ = "finish_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    # Relationships
    matches: Mapped[List["Match"]] = relationship(back_populates="finish_type")

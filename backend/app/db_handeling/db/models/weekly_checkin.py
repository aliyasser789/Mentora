from __future__ import annotations

import uuid

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db_handeling.db import Base


class WeeklyCheckin(Base):
    __tablename__ = "weekly_checkins"
    __table_args__ = (
        UniqueConstraint("user_id", "week_start_date", name="uq_weekly_checkins_user_week"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    roadmap_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roadmaps.id", ondelete="RESTRICT"),
        nullable=True,
    )
    week_start_date = Column(Date, nullable=False, index=True)
    progress_percent = Column(Float, nullable=True)
    reflection_notes = Column(Text, nullable=True)
    confidence_delta = Column(Float, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("User")
    roadmap = relationship("Roadmap")

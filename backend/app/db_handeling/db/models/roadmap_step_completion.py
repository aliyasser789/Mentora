from __future__ import annotations

import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db_handeling.db import Base


class RoadmapStepCompletion(Base):
    __tablename__ = "roadmap_step_completion"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "roadmap_step_id",
            name="uq_roadmap_step_completion_user_id_roadmap_step_id",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    roadmap_step_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roadmap_steps.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status = Column(
        String(50),
        nullable=False,
        default="not_started",
        server_default=text("'not_started'"),
        index=True,
    )
    completed_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
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
    roadmap_step = relationship("RoadmapStep", back_populates="completions")

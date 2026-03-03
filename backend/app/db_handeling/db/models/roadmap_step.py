from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db_handeling.db import Base


class RoadmapStep(Base):
    __tablename__ = "roadmap_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roadmaps.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("skills.id", ondelete="RESTRICT"),
        nullable=True,
    )
    week_number = Column(Integer, nullable=True, index=True)
    step_order = Column(Integer, nullable=False, index=True)
    estimated_hours = Column(Integer, nullable=True)
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

    roadmap = relationship("Roadmap", back_populates="steps")
    skill = relationship("Skill")
    completions = relationship("RoadmapStepCompletion", back_populates="roadmap_step")

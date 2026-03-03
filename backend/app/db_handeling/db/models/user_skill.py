from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db_handeling.db import Base


class UserSkill(Base):
    __tablename__ = "user_skills"
    __table_args__ = (
        Index(
            "uq_user_skills_user_id_skill_id_active",
            "user_id",
            "skill_id",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("skills.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    confidence_score = Column(
        Float,
        nullable=False,
        default=0.0,
        server_default=text("0.0"),
        index=True,
    )
    evidence_count = Column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )
    extraction_method = Column(String(50), nullable=True)
    model_version = Column(String(50), nullable=True)
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
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")
    skill = relationship("Skill", back_populates="user_skills")

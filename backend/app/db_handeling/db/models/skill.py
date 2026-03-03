from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, Index, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db_handeling.db import Base


class Skill(Base):
    __tablename__ = "skills"
    __table_args__ = (
        Index(
            "uq_skills_normalized_name_active",
            "normalized_name",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    normalized_name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
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

    aliases = relationship("SkillAlias", back_populates="skill")
    user_skills = relationship("UserSkill", back_populates="skill")

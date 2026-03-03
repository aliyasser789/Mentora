from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db_handeling.db import Base


class JobPostingSkill(Base):
    __tablename__ = "job_posting_skills"
    __table_args__ = (
        UniqueConstraint(
            "job_posting_id",
            "skill_id",
            name="uq_job_posting_skills_job_posting_id_skill_id",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_posting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("job_postings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("skills.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    extraction_method = Column(String(50), nullable=True)
    model_version = Column(String(50), nullable=True)
    confidence = Column(Float, nullable=True)
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

    job_posting = relationship("JobPosting", back_populates="job_posting_skills")
    skill = relationship("Skill")

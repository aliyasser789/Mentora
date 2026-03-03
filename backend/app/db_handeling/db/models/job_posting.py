from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, Index, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db_handeling.db import Base


class JobPosting(Base):
    __tablename__ = "job_postings"
    __table_args__ = (
        Index(
            "uq_job_postings_source_external_id_active",
            "source",
            "external_id",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
        Index("ix_job_postings_source_external_id", "source", "external_id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String(50), nullable=False, index=True)
    external_id = Column(String(128), nullable=False)
    title = Column(String(500), nullable=False)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    country = Column(String(80), nullable=True)
    city = Column(String(120), nullable=True)
    employment_type = Column(String(80), nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    currency = Column(String(10), nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True, index=True)
    url = Column(String(800), nullable=True)
    description = Column(Text, nullable=True)
    raw_json = Column(JSONB, nullable=False)
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

    job_posting_skills = relationship("JobPostingSkill", back_populates="job_posting")

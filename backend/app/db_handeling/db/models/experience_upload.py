from __future__ import annotations

import uuid

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db_handeling.db import Base


class ExperienceUpload(Base):
    __tablename__ = "experience_uploads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    title = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=False, index=True)
    start_date = Column(Date, nullable=True, index=True)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    original_filename = Column(String(255), nullable=True)
    mime_type = Column(String(100), nullable=True)
    file_size_bytes = Column(BigInteger, nullable=True)
    text_extracted = Column(Text, nullable=True)
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

    user = relationship("User", back_populates="experience_uploads")

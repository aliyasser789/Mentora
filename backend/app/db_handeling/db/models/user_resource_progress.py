from __future__ import annotations

import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db_handeling.db import Base


class UserResourceProgress(Base):
    __tablename__ = "user_resource_progress"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "resource_id",
            name="uq_user_resource_progress_user_id_resource_id",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    resource_id = Column(
        UUID(as_uuid=True),
        ForeignKey("resources.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status = Column(
        String(50),
        nullable=False,
        default="not_started",
        server_default=text("'not_started'"),
    )
    progress_percent = Column(Float, nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
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
    resource = relationship("Resource", back_populates="user_progress")

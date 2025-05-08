from datetime import datetime
from typing import Optional
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import UUID, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column


class AuditMixin:
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

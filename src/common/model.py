
from sqlalchemy import Column, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    id: Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True)
import uuid

from sqlalchemy import Date, ForeignKey, Integer, String, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AppBase


class Event(AppBase):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(120))
    date: Mapped[Date]
    start_time: Mapped[Time | None]
    end_time: Mapped[Time | None]
    capacity: Mapped[int | None] = mapped_column(Integer)
    location: Mapped[str | None] = mapped_column(String(120))
    vendor_name: Mapped[str | None] = mapped_column(String(120))
    poll_option_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("poll_options.id"))

    poll_option = relationship("PollOption")

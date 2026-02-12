import uuid

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AppBase


class Poll(AppBase):
    __tablename__ = "polls"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(120))
    month: Mapped[Date]
    description: Mapped[str | None] = mapped_column(String(255))

    options: Mapped[list["PollOption"]] = relationship(back_populates="poll", cascade="all, delete-orphan")


class PollOption(AppBase):
    __tablename__ = "poll_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    poll_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("polls.id", ondelete="CASCADE"))
    label: Mapped[str] = mapped_column(String(120))
    capacity: Mapped[int | None] = mapped_column(Integer)
    tags: Mapped[str | None] = mapped_column(String(120))

    poll: Mapped[Poll] = relationship(back_populates="options")
    votes: Mapped[list["PollVote"]] = relationship(back_populates="option", cascade="all, delete-orphan")


class PollVote(AppBase):
    __tablename__ = "poll_votes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    poll_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("polls.id", ondelete="CASCADE"))
    option_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("poll_options.id", ondelete="CASCADE"))
    resident_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("residents.id"))
    priority: Mapped[int] = mapped_column(Integer, default=1)

    option: Mapped[PollOption] = relationship(back_populates="votes")

import uuid
from datetime import datetime, timedelta

from sqlalchemy import DateTime, ForeignKey, Interval, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AppBase


class StaffMember(AppBase):
    __tablename__ = "staff_members"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("user_accounts.id"))
    first_name: Mapped[str] = mapped_column(String(80))
    last_name: Mapped[str] = mapped_column(String(80))
    role: Mapped[str] = mapped_column(String(64))
    certifications: Mapped[str | None] = mapped_column(String(255))

    shifts: Mapped[list["StaffShift"]] = relationship(back_populates="staff")
    account = relationship("UserAccount", back_populates="staff_profile")


class StaffShift(AppBase):
    __tablename__ = "staff_shifts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("staff_members.id"))
    start_at: Mapped[datetime] = mapped_column(DateTime)
    end_at: Mapped[datetime] = mapped_column(DateTime)
    break_duration: Mapped[timedelta | None] = mapped_column(Interval)

    staff: Mapped[StaffMember] = relationship(back_populates="shifts")

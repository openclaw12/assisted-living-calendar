import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AppBase


class AccountRole(str, enum.Enum):
    business = "business"
    employee = "employee"
    resident = "resident"


class UserAccount(AppBase):
    __tablename__ = "user_accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(String(160), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[AccountRole] = mapped_column(Enum(AccountRole, name="account_role"))
    display_name: Mapped[str | None] = mapped_column(String(120))

    organization = relationship("Organization", back_populates="accounts")
    resident_profile = relationship("Resident", back_populates="account", uselist=False)
    staff_profile = relationship("StaffMember", back_populates="account", uselist=False)

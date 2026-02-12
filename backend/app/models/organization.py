import uuid

from slugify import slugify
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AppBase


class Organization(AppBase):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(140), unique=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True)
    subscription_status: Mapped[str] = mapped_column(String(32), default="active")

    accounts: Mapped[list["UserAccount"]] = relationship(back_populates="organization", cascade="all, delete-orphan")

    def set_slug(self) -> None:
        if not self.slug:
            self.slug = slugify(self.name)

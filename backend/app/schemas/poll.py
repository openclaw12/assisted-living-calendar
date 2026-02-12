from __future__ import annotations

import uuid
from datetime import date

from pydantic import BaseModel


class PollOptionCreate(BaseModel):
    label: str
    capacity: int | None = None
    tags: str | None = None


class PollCreate(BaseModel):
    title: str
    month: date
    description: str | None = None
    options: list[PollOptionCreate]


class PollVoteCreate(BaseModel):
    option_id: uuid.UUID
    resident_id: uuid.UUID
    priority: int = 1


class PollOptionResponse(BaseModel):
    id: uuid.UUID
    label: str
    capacity: int | None = None
    tags: str | None = None
    votes: int


class PollResponse(BaseModel):
    id: uuid.UUID
    title: str
    month: date
    description: str | None = None
    options: list[PollOptionResponse]

    class Config:
        from_attributes = True

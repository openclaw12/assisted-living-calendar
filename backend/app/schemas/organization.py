import uuid

from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    subscription_status: str

    class Config:
        from_attributes = True

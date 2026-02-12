import uuid

from pydantic import BaseModel, EmailStr

from app.models.user_account import AccountRole


class SignupRequest(BaseModel):
    organization_id: uuid.UUID
    email: EmailStr
    password: str
    display_name: str
    role: AccountRole

    # optional metadata for residents/employees
    resident_first_name: str | None = None
    resident_last_name: str | None = None
    staff_first_name: str | None = None
    staff_last_name: str | None = None
    staff_role: str | None = None


class SignupResponse(BaseModel):
    account_id: uuid.UUID
    role: AccountRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    account_id: uuid.UUID
    role: AccountRole

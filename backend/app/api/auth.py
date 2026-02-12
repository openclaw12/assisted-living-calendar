import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.db.session import get_session
from app.models import AccountRole, Organization, Resident, StaffMember, UserAccount
from app.schemas import LoginRequest, LoginResponse, SignupRequest, SignupResponse

router = APIRouter()


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, session: Session = Depends(get_session)) -> SignupResponse:
    org = session.get(Organization, payload.organization_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    existing = session.scalar(select(UserAccount).where(UserAccount.email == payload.email))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")

    account = UserAccount(
        organization_id=payload.organization_id,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        display_name=payload.display_name,
    )
    session.add(account)
    session.flush()

    if payload.role == AccountRole.resident:
        if not payload.resident_first_name or not payload.resident_last_name:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Resident name required")
        resident = Resident(
            account_id=account.id,
            first_name=payload.resident_first_name,
            last_name=payload.resident_last_name,
            birth_date=None,
        )
        session.add(resident)
    elif payload.role == AccountRole.employee:
        if not payload.staff_first_name or not payload.staff_last_name:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Staff name required")
        staff = StaffMember(
            account_id=account.id,
            first_name=payload.staff_first_name,
            last_name=payload.staff_last_name,
            role=payload.staff_role or "Caregiver",
        )
        session.add(staff)

    session.commit()
    return SignupResponse(account_id=account.id, role=account.role)


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)) -> LoginResponse:
    account = session.scalar(select(UserAccount).where(UserAccount.email == payload.email))
    if not account or not verify_password(payload.password, account.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = secrets.token_urlsafe(24)
    return LoginResponse(token=token, account_id=account.id, role=account.role)

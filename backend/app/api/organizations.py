import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.qr import generate_qr_data_uri
from app.db.session import get_session
from app.models import Organization
from app.schemas import OrganizationCreate, OrganizationResponse

router = APIRouter()


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_org(payload: OrganizationCreate, session: Session = Depends(get_session)) -> OrganizationResponse:
    existing = session.scalar(select(Organization).where(Organization.name == payload.name))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Organization already exists")
    org = Organization(name=payload.name, slug=slugify(payload.name))
    session.add(org)
    session.commit()
    session.refresh(org)
    return OrganizationResponse.model_validate(org)


@router.get("/", response_model=list[OrganizationResponse])
def list_orgs(session: Session = Depends(get_session)) -> list[OrganizationResponse]:
    orgs = session.scalars(select(Organization)).all()
    return [OrganizationResponse.model_validate(org) for org in orgs]


@router.get("/slug/{slug}", response_model=OrganizationResponse)
def get_org_by_slug(slug: str, session: Session = Depends(get_session)) -> OrganizationResponse:
    org = session.scalar(select(Organization).where(Organization.slug == slug))
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return OrganizationResponse.model_validate(org)


@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_org(organization_id: uuid.UUID, session: Session = Depends(get_session)) -> OrganizationResponse:
    org = session.get(Organization, organization_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return OrganizationResponse.model_validate(org)


def _build_signup_url(request: Request, organization: Organization, role: str) -> str:
    base = str(request.base_url).rstrip("/")
    return f"{base}/signup/{organization.slug}/{role}"


@router.post("/{organization_id}/qr-links")
def generate_qr_links(
    organization_id: uuid.UUID, request: Request, session: Session = Depends(get_session)
) -> dict[str, str]:
    org = session.get(Organization, organization_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    employee_url = _build_signup_url(request, org, "employee")
    resident_url = _build_signup_url(request, org, "resident")
    return {
        "employee_signup_url": employee_url,
        "resident_signup_url": resident_url,
        "employee_qr": generate_qr_data_uri(employee_url),
        "resident_qr": generate_qr_data_uri(resident_url),
    }

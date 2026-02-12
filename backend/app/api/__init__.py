from fastapi import APIRouter

from . import auth, events, polls, residents, staff, vendors, analytics, organizations

router = APIRouter(prefix="/api")
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
router.include_router(residents.router, prefix="/residents", tags=["residents"])
router.include_router(staff.router, prefix="/staff", tags=["staff"])
router.include_router(polls.router, prefix="/polls", tags=["polls"])
router.include_router(events.router, prefix="/events", tags=["events"])
router.include_router(vendors.router, prefix="/vendors", tags=["vendors"])
router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

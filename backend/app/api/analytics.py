from fastapi import APIRouter

router = APIRouter()


@router.get("/engagement")
def engagement_summary() -> dict:
    return {"engagementScore": 0}

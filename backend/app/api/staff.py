from fastapi import APIRouter

router = APIRouter()


@router.get("/shifts")
def list_shifts() -> list[dict]:
    return []

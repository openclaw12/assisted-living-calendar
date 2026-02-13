from fastapi import FastAPI

from .api import router as api_router
from .db.init_db import init_db

init_db()

app = FastAPI(title="Assisted Living Calendar API", version="0.1.0")
app.include_router(api_router)


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}

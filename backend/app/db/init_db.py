from app.db.session import engine
from app.db.base import Base
import app.models  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

import pytest
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User


@pytest.fixture
def db():
    session: Session = SessionLocal()

    try:
        yield session
    finally:
        session.query(User).delete()
        session.commit()
        session.close()
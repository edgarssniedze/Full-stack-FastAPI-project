from datetime import datetime
from sqlmodel import Session, select
from app.models.role import Role

def seed_roles(session: Session):
    existing = session.exec(select(Role)).all()

    if existing:
        return

    roles = [
        Role(
            name="admin",
            description="administrator",
            created=datetime.now()
        ),
        Role(
            name="user",
            description="regular user",
            created=datetime.now()
        )
    ]

    session.add_all(roles)
    session.commit()
from database import SessionLocal
from models import Admin, University


def is_admin(telegram_id: str):
    db = SessionLocal()
    admin = db.query(Admin).filter_by(telegram_id=str(telegram_id)).first()
    return admin is not None


def add_admin(telegram_id: str, university_id: int):
    db = SessionLocal()
    admin = Admin(
        telegram_id=str(telegram_id),
        university_id=university_id
    )
    db.add(admin)
    db.commit()


def create_university(name, api_url, api_token):
    db = SessionLocal()
    uni = University(
        name=name,
        api_url=api_url,
        api_token=api_token
    )
    db.add(uni)
    db.commit()
    return uni.id
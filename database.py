from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///students.db")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


from models import University


def add_university(name, api_url, api_token, admin_id):

    db = SessionLocal()

    uni = University(
        name=name,
        api_url=api_url,
        api_token=api_token,
        admin_id=admin_id
    )

    db.add(uni)
    db.commit()


def get_university_by_admin(admin_id):

    db = SessionLocal()

    return db.query(University).filter_by(
        admin_id=admin_id
    ).first()
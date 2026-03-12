from sqlalchemy import Column, Integer, String
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    jshshir = Column(String)

    contract_debt = Column(Integer)
    credit_debt = Column(Integer)
    library_debt = Column(Integer)
    dorm_debt = Column(Integer)

    telegram_id = Column(String)


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    api_url = Column(String)
    api_token = Column(String)

    admin_id = Column(Integer)
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


# =========================
# STUDENT
# =========================
class Student(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    surname = Column(String)

    father_name = Column(String)

    university = Column(String)

    direction = Column(String)

    course = Column(Integer)

    group = Column(String)

    jshshir = Column(String, unique=True)

    telegram_id = Column(String)

    contract_debt = Column(Integer, default=0)

    credit_debt = Column(Integer, default=0)

    library_debt = Column(Integer, default=0)

    dorm_debt = Column(Integer, default=0)

    messages_sent = Column(Integer, default=0)


# =========================
# UNIVERSITY
# =========================
class University(Base):

    __tablename__ = "universities"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    api_url = Column(String)

    api_token = Column(String)


# =========================
# ADMIN
# =========================
class Admin(Base):

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)

    telegram_id = Column(String, unique=True)

    university_id = Column(Integer, ForeignKey("universities.id"))
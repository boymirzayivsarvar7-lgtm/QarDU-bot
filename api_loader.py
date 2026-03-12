import json
from database import SessionLocal
from models import Student


def load_students():

    db = SessionLocal()

    with open("test_students.json", "r", encoding="utf-8") as f:
        students = json.load(f)

    for s in students:

        student = db.query(Student).filter_by(
            jshshir=s["jshshir"]
        ).first()

        if not student:

            new_student = Student(
                name=s["name"],
                jshshir=s["jshshir"],
                contract_debt=s["contract_debt"],
                credit_debt=s["credit_debt"],
                library_debt=s["library_debt"],
                dorm_debt=s["dorm_debt"]
            )

            db.add(new_student)

    db.commit()

    print("Talabalar JSON fayldan yuklandi")
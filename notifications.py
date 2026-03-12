import asyncio
from database import SessionLocal
from models import Student


async def send_notifications(bot):

    db = SessionLocal()

    students = db.query(Student).all()

    for s in students:

        if not s.telegram_id:
            continue

        messages = []

        if s.contract_debt > 0:
            messages.append(f"Kontrakt qarzdorligi: {s.contract_debt} so'm")

        if s.credit_debt > 0:
            messages.append(f"Kredit qarzdorligi: {s.credit_debt}")

        if s.library_debt > 0:
            messages.append("Kutubxona qarzdorligi mavjud")

        if s.dorm_debt > 0:
            messages.append("Yotoqxona qarzdorligi mavjud")

        if messages:

            text = (
                f"Hurmatli {s.name}!\n\n"
                "Sizda quyidagi qarzdorliklar mavjud:\n\n"
                + "\n".join(messages)
            )

            await bot.send_message(s.telegram_id, text)

            await asyncio.sleep(0.1)
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN
from database import Base, engine, SessionLocal
from models import Student
from settings import is_admin, add_admin, create_university


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

Base.metadata.create_all(engine)

waiting_university = {}
waiting_jshshir = set()


# =========================
# TALABA MENYU
# =========================
student_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Qarzdorligim")],
        [KeyboardButton(text="👤 Men haqimda")],
        [KeyboardButton(text="ℹ️ Ma'lumot"), KeyboardButton(text="☎️ Aloqa")]
    ],
    resize_keyboard=True
)


# =========================
# ADMIN MENYU
# =========================
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏫 Universitet qo'shish")],
        [KeyboardButton(text="📊 Statistika")]
    ],
    resize_keyboard=True
)


# =========================
# START
# =========================
@dp.message(CommandStart())
async def start(message: types.Message):

    waiting_jshshir.add(message.from_user.id)

    await message.answer(
        "Assalomu alaykum!\n\n"
        "JSHSHIR raqamingizni kiriting"
    )


# =========================
# ADMIN PANEL
# =========================
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):

    if not is_admin(message.from_user.id):

        await message.answer(
            "Siz admin emassiz.\n"
            "Agar universitet admini bo‘lsangiz "
            "avval universitet qo‘shing."
        )

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🏫 Universitet qo'shish")]
            ],
            resize_keyboard=True
        )

        await message.answer("Universitet qo'shish:", reply_markup=keyboard)

        return

    await message.answer(
        "Admin panel",
        reply_markup=admin_menu
    )


# =========================
# UNIVERSITET QO‘SHISH BOSHLASH
# =========================
@dp.message(lambda m: m.text == "🏫 Universitet qo'shish")
async def add_university_start(message: types.Message):

    waiting_university[message.from_user.id] = {"step": "name"}

    await message.answer("Universitet nomini kiriting")


# =========================
# UNIVERSITET MA'LUMOTLARI
# =========================
@dp.message()
async def university_setup(message: types.Message):

    uid = message.from_user.id

    if uid in waiting_university:

        data = waiting_university[uid]

        if data["step"] == "name":

            data["name"] = message.text
            data["step"] = "api"

            await message.answer("API URL kiriting")

            return

        elif data["step"] == "api":

            data["api"] = message.text
            data["step"] = "token"

            await message.answer("API TOKEN kiriting")

            return

        elif data["step"] == "token":

            uni_id = create_university(
                data["name"],
                data["api"],
                message.text
            )

            add_admin(uid, uni_id)

            del waiting_university[uid]

            await message.answer(
                "Universitet muvaffaqiyatli qo'shildi\n"
                "Siz endi admin bo'ldingiz",
                reply_markup=admin_menu
            )

            return


# =========================
# JSHSHIR
# =========================
    if message.text.startswith("/"):
        return

    user_id = message.from_user.id

    if user_id not in waiting_jshshir:
        return

    db = SessionLocal()

    student = db.query(Student).filter_by(
        jshshir=message.text
    ).first()

    if student:

        student.telegram_id = str(user_id)

        db.commit()

        waiting_jshshir.remove(user_id)

        await message.answer(
            f"""
Hurmatli {student.name}!

Siz tizimga muvaffaqiyatli ulandingiz.
""",
            reply_markup=student_menu
        )

    else:

        await message.answer("Bunday JSHSHIR topilmadi")


# =========================
# MAIN
# =========================
async def main():

    print("Bot ishga tushdi")

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
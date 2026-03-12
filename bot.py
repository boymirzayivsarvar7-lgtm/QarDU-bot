import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from config import BOT_TOKEN
from database import Base, engine, SessionLocal, add_university, get_university_by_admin

from models import Student

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

Base.metadata.create_all(engine)


start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 Talaba")],
        [KeyboardButton(text="👨‍💼 Admin")]
    ],
    resize_keyboard=True
)


student_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Kontrakt qarzi")],
        [KeyboardButton(text="📚 Kredit qarzi")],
        [KeyboardButton(text="📖 Kutubxona qarzi")],
        [KeyboardButton(text="🏠 Yotoqxona qarzi")]
    ],
    resize_keyboard=True
)


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏫 Universitet qo'shish")],
        [KeyboardButton(text="📢 Xabar yuborish")],
        [KeyboardButton(text="📊 Statistika")]
    ],
    resize_keyboard=True
)


waiting_jshshir = set()

waiting_university = {}


@dp.message(CommandStart())
async def start(message: types.Message):

    await message.answer(
        "Assalomu alaykum!\nKim sifatida kirasiz?",
        reply_markup=start_menu
    )


@dp.message(lambda m: m.text == "🎓 Talaba")
async def student_start(message: types.Message):

    waiting_jshshir.add(message.from_user.id)

    await message.answer("JSHSHIR raqamingizni kiriting")


@dp.message(lambda m: m.text == "👨‍💼 Admin")
async def admin_start(message: types.Message):

    university = get_university_by_admin(message.from_user.id)

    if university:

        await message.answer(
            "Admin panelga xush kelibsiz",
            reply_markup=admin_menu
        )

    else:

        await message.answer(
            "Siz admin emassiz.\nUniversitet qo'shishingiz mumkin."
        )


@dp.message(lambda m: m.text == "🏫 Universitet qo'shish")
async def add_university_start(message: types.Message):

    waiting_university[message.from_user.id] = {"step": "name"}

    await message.answer("Universitet nomini kiriting")


@dp.message()
async def university_steps(message: types.Message):

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

            add_university(
                data["name"],
                data["api"],
                message.text,
                uid
            )

            del waiting_university[uid]

            await message.answer(
                "Universitet qo'shildi.\nSiz admin bo'ldingiz",
                reply_markup=admin_menu
            )

            return


    if message.from_user.id not in waiting_jshshir:
        return

    db = SessionLocal()

    student = db.query(Student).filter_by(
        jshshir=message.text
    ).first()

    if student:

        student.telegram_id = str(message.from_user.id)
        db.commit()

        waiting_jshshir.remove(message.from_user.id)

        await message.answer(
            f"{student.name}\nSiz tizimga ulandingiz",
            reply_markup=student_menu
        )

    else:

        await message.answer("Bunday JSHSHIR topilmadi")


async def main():

    print("Bot ishga tushdi")

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
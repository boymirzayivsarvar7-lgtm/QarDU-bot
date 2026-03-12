import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiohttp import web

from config import BOT_TOKEN, ADMINS
from database import Base, engine, SessionLocal
from models import Student

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

Base.metadata.create_all(engine)

waiting_jshshir = set()

# ===== MENYU =====

student_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Kontrakt qarzi")],
        [KeyboardButton(text="📚 Kredit qarzi")],
        [KeyboardButton(text="📖 Kutubxona qarzi")],
        [KeyboardButton(text="🏠 Yotoqxona qarzi")],
        [KeyboardButton(text="👤 Men haqimda")]
    ],
    resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📢 Xabar yuborish")],
        [KeyboardButton(text="📊 Statistika")],
    ],
    resize_keyboard=True
)


# ===== START =====

@dp.message(CommandStart())
async def start(message: types.Message):

    if message.from_user.id in ADMINS:
        await message.answer("Admin panelga xush kelibsiz", reply_markup=admin_menu)
        return

    waiting_jshshir.add(message.from_user.id)

    await message.answer(
        "Assalomu alaykum!\n\n"
        "JSHSHIR raqamingizni kiriting:"
    )


# ===== JSHSHIR KIRITISH =====

@dp.message()
async def get_jshshir(message: types.Message):

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
            f"Hurmatli {student.name}\n"
            f"Siz tizimga muvaffaqiyatli ulandingiz",
            reply_markup=student_menu
        )

    else:

        await message.answer("Bunday JSHSHIR topilmadi")


# ===== QARZLAR =====

@dp.message(lambda message: message.text == "💰 Kontrakt qarzi")
async def contract_debt(message: types.Message):

    db = SessionLocal()

    student = db.query(Student).filter_by(
        telegram_id=str(message.from_user.id)
    ).first()

    await message.answer(
        f"Kontrakt qarzingiz: {student.contract_debt} so'm"
    )


@dp.message(lambda message: message.text == "📚 Kredit qarzi")
async def credit_debt(message: types.Message):

    db = SessionLocal()

    student = db.query(Student).filter_by(
        telegram_id=str(message.from_user.id)
    ).first()

    await message.answer(
        f"Kredit qarzingiz: {student.credit_debt}"
    )


@dp.message(lambda message: message.text == "📖 Kutubxona qarzi")
async def library_debt(message: types.Message):

    db = SessionLocal()

    student = db.query(Student).filter_by(
        telegram_id=str(message.from_user.id)
    ).first()

    await message.answer(
        f"Kutubxona qarzingiz: {student.library_debt}"
    )


@dp.message(lambda message: message.text == "🏠 Yotoqxona qarzi")
async def dorm_debt(message: types.Message):

    db = SessionLocal()

    student = db.query(Student).filter_by(
        telegram_id=str(message.from_user.id)
    ).first()

    await message.answer(
        f"Yotoqxona qarzingiz: {student.dorm_debt}"
    )


# ===== MEN HAQIMDA =====

@dp.message(lambda message: message.text == "👤 Men haqimda")
async def about_me(message: types.Message):

    db = SessionLocal()

    student = db.query(Student).filter_by(
        telegram_id=str(message.from_user.id)
    ).first()

    await message.answer(
        f"👤 Ism: {student.name}\n"
        f"🆔 JSHSHIR: {student.jshshir}\n"
        f"🎓 Universitet: QarDU\n"
        f"📚 Yo'nalish: Dasturiy injiniring\n"
        f"🏫 Kurs: 2-kurs\n"
        f"👥 Guruh: 21-01"
    )


# ===== RENDER UCHUN WEB SERVER =====

async def handle(request):
    return web.Response(text="Bot ishlayapti")


async def start_web():

    port = int(os.environ.get("PORT", 10000))

    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()


# ===== BOTNI ISHGA TUSHIRISH =====

async def main():

    print("Bot ishga tushdi")

    await start_web()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
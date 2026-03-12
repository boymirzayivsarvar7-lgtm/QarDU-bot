import asyncio
import requests

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from config import BOT_TOKEN
from database import SessionLocal
from models import University

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_state = {}
admin_data = {}

# START MENU
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 Talaba")],
        [KeyboardButton(text="👨‍💼 Admin")]
    ],
    resize_keyboard=True
)

# ADMIN PANEL
admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="📢 Xabar yuborish")]
    ],
    resize_keyboard=True
)


# START
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum!\nKim sifatida kirasiz?",
        reply_markup=start_kb
    )


# TALABA
@dp.message(F.text == "🎓 Talaba")
async def student(message: types.Message):
    user_state[message.from_user.id] = "student_jshshir"

    await message.answer("JSHSHIR raqamingizni kiriting")


# TALABA JSHSHIR
@dp.message()
async def student_jshshir(message: types.Message):

    if user_state.get(message.from_user.id) != "student_jshshir":
        return

    jshshir = message.text

    db = SessionLocal()
    uni = db.query(University).first()
    db.close()

    if not uni:
        await message.answer("Universitet hali qo'shilmagan")
        return

    try:
        headers = {"Authorization": f"Bearer {uni.api_token}"}
        r = requests.get(f"{uni.api_url}/{jshshir}", headers=headers)

        if r.status_code != 200:
            await message.answer("Bunday JSHSHIR topilmadi")
            return

        data = r.json()

        text = f"""
👤 FIO: {data.get("name")}
🎓 Fakultet: {data.get("faculty")}
📚 Kurs: {data.get("course")}
💰 Qarzdorlik: {data.get("debt")}
"""

        await message.answer(text)

    except:
        await message.answer("API ishlamayapti")

    user_state.pop(message.from_user.id)


# ADMIN BOSISH
@dp.message(F.text == "👨‍💼 Admin")
async def admin(message: types.Message):

    db = SessionLocal()
    uni = db.query(University).filter(
        University.admin_id == message.from_user.id
    ).first()
    db.close()

    if uni:
        await message.answer(
            "Admin panelga xush kelibsiz",
            reply_markup=admin_kb
        )
        return

    user_state[message.from_user.id] = "add_university"

    await message.answer("Universitet nomini kiriting")


# UNIVERSITET NOMI
@dp.message()
async def add_uni_name(message: types.Message):

    if user_state.get(message.from_user.id) != "add_university":
        return

    admin_data[message.from_user.id] = {}
    admin_data[message.from_user.id]["name"] = message.text

    user_state[message.from_user.id] = "api_url"

    await message.answer("API URL kiriting")


# API URL
@dp.message()
async def add_api(message: types.Message):

    if user_state.get(message.from_user.id) != "api_url":
        return

    admin_data[message.from_user.id]["api_url"] = message.text
    user_state[message.from_user.id] = "api_token"

    await message.answer("API TOKEN kiriting")


# API TOKEN
@dp.message()
async def add_token(message: types.Message):

    if user_state.get(message.from_user.id) != "api_token":
        return

    admin_data[message.from_user.id]["api_token"] = message.text

    data = admin_data[message.from_user.id]

    db = SessionLocal()

    uni = University(
        name=data["name"],
        api_url=data["api_url"],
        api_token=data["api_token"],
        admin_id=message.from_user.id
    )

    db.add(uni)
    db.commit()
    db.close()

    await message.answer(
        "Universitet muvaffaqiyatli qo'shildi",
        reply_markup=admin_kb
    )

    user_state.pop(message.from_user.id)
    admin_data.pop(message.from_user.id)


# STATISTIKA
@dp.message(F.text == "📊 Statistika")
async def stat(message: types.Message):
    await message.answer("Statistika hozircha yo'q")


# XABAR
@dp.message(F.text == "📢 Xabar yuborish")
async def send_msg(message: types.Message):

    user_state[message.from_user.id] = "send_msg"

    await message.answer("Talabalarga yuboriladigan xabarni kiriting")


@dp.message()
async def send_all(message: types.Message):

    if user_state.get(message.from_user.id) != "send_msg":
        return

    await message.answer("Xabar yuborildi")

    user_state.pop(message.from_user.id)


# START BOT
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
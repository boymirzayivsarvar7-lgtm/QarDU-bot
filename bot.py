import asyncio
import requests

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN
from database import SessionLocal
from models import University


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_state = {}
admin_temp = {}


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 Talaba")],
        [KeyboardButton(text="👨‍💼 Admin")]
    ],
    resize_keyboard=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="📢 Xabar yuborish")]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: types.Message):

    user_state.pop(message.from_user.id, None)

    await message.answer(
        "Assalomu alaykum!\nKim sifatida kirasiz?",
        reply_markup=start_kb
    )


# TALABA
@dp.message(F.text == "🎓 Talaba")
async def talaba(message: types.Message):

    user_state.pop(message.from_user.id, None)

    user_state[message.from_user.id] = "jshshir"

    await message.answer("JSHSHIR kiriting")


# ADMIN
@dp.message(F.text == "👨‍💼 Admin")
async def admin(message: types.Message):

    user_state.pop(message.from_user.id, None)

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
    else:
        user_state[message.from_user.id] = "uni_name"

        await message.answer("Universitet nomini kiriting")


# UNIVERSITET NOMI
@dp.message()
async def uni_name(message: types.Message):

    if user_state.get(message.from_user.id) != "uni_name":
        return

    admin_temp[message.from_user.id] = {"name": message.text}

    user_state[message.from_user.id] = "api_url"

    await message.answer("API URL kiriting")


# API URL
@dp.message()
async def api_url(message: types.Message):

    if user_state.get(message.from_user.id) != "api_url":
        return

    admin_temp[message.from_user.id]["api_url"] = message.text

    user_state[message.from_user.id] = "api_token"

    await message.answer("API TOKEN kiriting")


# API TOKEN
@dp.message()
async def api_token(message: types.Message):

    if user_state.get(message.from_user.id) != "api_token":
        return

    admin_temp[message.from_user.id]["api_token"] = message.text

    data = admin_temp[message.from_user.id]

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
    admin_temp.pop(message.from_user.id)


# TALABA JSHSHIR
@dp.message()
async def student_jshshir(message: types.Message):

    if user_state.get(message.from_user.id) != "jshshir":
        return

    jshshir = message.text

    db = SessionLocal()
    uni = db.query(University).first()
    db.close()

    if not uni:
        await message.answer("Universitet mavjud emas")
        return

    try:

        headers = {
            "Authorization": f"Bearer {uni.api_token}"
        data = {
            "name": "Test Talaba",
            "faculty": "Axborot texnologiyalari",
            "course": 3,
            "debt": 0
        }
        }

        # r = requests.get(
        #     f"{uni.api_url}/{jshshir}",
        #     headers=headers
        # )

        # if r.status_code != 200:
        #     await message.answer("Bunday JSHSHIR topilmadi")
        #     return

        # data = r.json()

        text = f"""
        👤 FIO: {data.get("name")}
        🎓 Fakultet: {data.get("faculty")}
        📚 Kurs: {data.get("course")}
        💰 Qarzdorlik: {data.get("debt")}
        """

        await message.answer(text)

    except Exception as e:

        print(e)

        await message.answer("API ishlamayapti")

    user_state.pop(message.from_user.id)


# STATISTIKA
@dp.message(F.text == "📊 Statistika")
async def stat(message: types.Message):
    await message.answer("Statistika hozircha yo'q")


# XABAR YUBORISH
@dp.message(F.text == "📢 Xabar yuborish")
async def send_msg(message: types.Message):

    user_state[message.from_user.id] = "send"

    await message.answer("Yuboriladigan xabarni kiriting")


@dp.message()
async def send_all(message: types.Message):

    if user_state.get(message.from_user.id) != "send":
        return

    await message.answer("Xabar yuborildi")

    user_state.pop(message.from_user.id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
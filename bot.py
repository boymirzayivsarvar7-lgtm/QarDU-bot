import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from students import students

from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_state = {}
admin_data = {}


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 Talaba")],
        [KeyboardButton(text="👨‍💼 Admin")]
    ],
    resize_keyboard=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏫 Universitet qo'shish")],
        [KeyboardButton(text="📊 Statistika")]
    ],
    resize_keyboard=True
)


# START
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

    user_state[message.from_user.id] = "jshshir"

    await message.answer("JSHSHIR raqamingizni kiriting")


# ADMIN
@dp.message(F.text == "👨‍💼 Admin")
async def admin(message: types.Message):

    await message.answer(
        "Admin panelga xush kelibsiz",
        reply_markup=admin_kb
    )


# UNIVERSITET QO'SHISH
@dp.message(F.text == "🏫 Universitet qo'shish")
async def add_uni(message: types.Message):

    user_state[message.from_user.id] = "uni_name"

    await message.answer("Universitet nomini kiriting")


# UNIVERSITET NOMI
@dp.message()
async def uni_name(message: types.Message):

    if user_state.get(message.from_user.id) != "uni_name":
        return

    admin_data[message.from_user.id] = {
        "name": message.text
    }

    user_state[message.from_user.id] = "api_url"

    await message.answer("API URL kiriting (demo uchun har qanday yozing)")


# API URL
@dp.message()
async def api_url(message: types.Message):

    if user_state.get(message.from_user.id) != "api_url":
        return

    admin_data[message.from_user.id]["api_url"] = message.text

    user_state[message.from_user.id] = "api_token"

    await message.answer("API TOKEN kiriting (demo uchun har qanday yozing)")


# API TOKEN
@dp.message()
async def api_token(message: types.Message):

    if user_state.get(message.from_user.id) != "api_token":
        return

    admin_data[message.from_user.id]["api_token"] = message.text

    user_state.pop(message.from_user.id)

    await message.answer(
        "Universitet muvaffaqiyatli qo'shildi",
        reply_markup=admin_kb
    )


# STATISTIKA
@dp.message(F.text == "📊 Statistika")
async def stat(message: types.Message):

    await message.answer("Statistika hozircha mavjud emas")


# TALABA MA'LUMOTI (JSHSHIR)
@dp.message()
async def student(message: types.Message):

    if user_state.get(message.from_user.id) != "jshshir":
        return

    jshshir = message.text.strip()

    for s in students:

        if str(s["id"]) == jshshir:

            text = f"""
👤 FIO: {s["name"]}
🎓 Fakultet: {s["faculty"]}
📚 Kurs: {s["course"]}
💰 Qarzdorlik: {s["contract_debt"]} so'm
"""

            await message.answer(text)

            user_state.pop(message.from_user.id)
            return

    await message.answer("Talaba topilmadi")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
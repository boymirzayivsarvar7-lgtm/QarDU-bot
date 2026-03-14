import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN, ADMIN_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

user_state = {}

# TEST TALABALAR
students = [
{"jshshir":"1001","name":"Ali Valiyev","faculty":"IT","course":2,"debt":0,"reason":"yo'q"},
{"jshshir":"1002","name":"Vali Karimov","faculty":"IT","course":3,"debt":200000,"reason":"kontrakt"},
{"jshshir":"1003","name":"Hasan Aliyev","faculty":"Matematika","course":1,"debt":0,"reason":"yo'q"},
{"jshshir":"1004","name":"Bek Olimov","faculty":"Fizika","course":4,"debt":150000,"reason":"kontrakt"},
{"jshshir":"1005","name":"Jasur Tursunov","faculty":"IT","course":2,"debt":0,"reason":"yo'q"},
{"jshshir":"1006","name":"Nodir Ahmedov","faculty":"Kimyo","course":3,"debt":300000,"reason":"kontrakt"},
{"jshshir":"1007","name":"Akmal Rustamov","faculty":"Biologiya","course":1,"debt":0,"reason":"yo'q"},
{"jshshir":"1008","name":"Dilshod Xasanov","faculty":"IT","course":2,"debt":100000,"reason":"kontrakt"},
{"jshshir":"1009","name":"Otabek Rahimov","faculty":"Tarix","course":4,"debt":0,"reason":"yo'q"},
{"jshshir":"1010","name":"Sardor Karimov","faculty":"IT","course":3,"debt":250000,"reason":"kontrakt"}
]

# MENYU
start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(KeyboardButton("🎓 Talaba"))
start_kb.add(KeyboardButton("👨‍💼 Admin"))

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(KeyboardButton("📊 Statistika"))
admin_kb.add(KeyboardButton("📢 Qarzdorga xabar"))

# START
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum!\nKim sifatida kirasiz?",
        reply_markup=start_kb
    )

# TALABA
@dp.message_handler(lambda message: message.text == "🎓 Talaba")
async def talaba(message: types.Message):

    user_state[message.from_user.id] = "jshshir"

    await message.answer("JSHSHIR kiriting")

# ADMIN
@dp.message_handler(lambda message: message.text == "👨‍💼 Admin")
async def admin(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Siz admin emassiz")
        return

    await message.answer(
        "👨‍💼 Admin panel",
        reply_markup=admin_kb
    )

# STATISTIKA
@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def stat(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    total = len(students)
    debtors = len([s for s in students if s["debt"] > 0])
    clear = len([s for s in students if s["debt"] == 0])

    text = f"""
📊 Statistika

Talabalar soni: {total}

Qarzdorlar: {debtors}

Qarzsizlar: {clear}
"""

    await message.answer(text)

# QARZDORGA XABAR
@dp.message_handler(lambda message: message.text == "📢 Qarzdorga xabar")
async def send(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    for s in students:

        if s["debt"] > 0:

            await message.answer(
                f"{s['name']} ga xabar yuborildi\nQarz: {s['debt']} so'm"
            )

    await message.answer("📢 Barcha qarzdorlarga xabar yuborildi")

# TALABA JSHSHIR
@dp.message_handler()
async def student(message: types.Message):

    if user_state.get(message.from_user.id) != "jshshir":
        return

    jshshir = message.text

    student = next((s for s in students if s["jshshir"] == jshshir), None)

    if not student:

        await message.answer("❌ Talaba topilmadi")
        return

    text = f"""
👤 FIO: {student['name']}

🎓 Fakultet: {student['faculty']}

📚 Kurs: {student['course']}

💰 Qarzdorlik: {student['debt']} so'm

📄 Sababi: {student['reason']}
"""

    await message.answer(text)

    user_state.pop(message.from_user.id)

if name == "main":
    executor.start_polling(dp, skip_updates=True)
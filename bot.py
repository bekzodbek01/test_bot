import logging
import random
import os
import json
import time
from docx import Document

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

DATA_PATH = "data"
DB_FILE = "db.json"

# =========================
# SHORT
# =========================
def short(text, max_len=90):
    return text[:max_len] + "..." if len(text) > max_len else text

# =========================
# DB
# =========================
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

results = load_db()

# =========================
# DOCX
# =========================
def parse_docx(file_path):
    doc = Document(file_path)
    questions = []

    for table in doc.tables:
        for row in table.rows[1:]:
            cells = [cell.text.strip() for cell in row.cells]

            if len(cells) >= 5:
                question = cells[0]
                correct_text = cells[1]

                options = [cells[1], cells[2], cells[3], cells[4]]
                random.shuffle(options)

                correct_index = options.index(correct_text)

                questions.append({
                    "question": question,
                    "options": options,
                    "correct": correct_index
                })

    return questions

def load_all_questions():
    all_questions = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".docx"):
            path = os.path.join(DATA_PATH, file)
            qs = parse_docx(path)

            for q in qs:
                q["subject"] = file.replace(".docx", "")
                all_questions.append(q)

    return random.sample(all_questions, min(70, len(all_questions)))

# =========================
# USERS
# =========================
users = {}

def start_test(user):
    users[user.id] = {
        "questions": load_all_questions(),
        "index": 0,
        "correct": 0,
        "incorrect": 0,
        "subjects": {},
        "answers": [],
        "start_time": time.time(),
        "username": user.username,
        "fullname": user.full_name
    }

# =========================
# MENUS
# =========================
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🚀 Test boshlash")
    return kb

def test_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔁 Qaytadan boshlash")
    kb.add("🛑 Testni tugatish")
    kb.add("🏠 Menu")
    return kb

def result_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔁 Qaytadan boshlash")
    kb.add("🏠 Menu")
    return kb

# =========================
# SEND QUESTION
# =========================
async def send_question(chat_id, user_id):
    data = users.get(user_id)
    if not data:
        return

    if data["index"] >= len(data["questions"]):
        return await finish_test(chat_id, user_id)

    q = data["questions"][data["index"]]

    letters = ["A","B","C","D"]
    options = [f"{letters[i]}) {short(opt)}" for i, opt in enumerate(q["options"])]

    try:
        await bot.send_poll(
            chat_id=chat_id,
            question=f"{data['index']+1}/70\n📚 {q['subject']}\n\n{short(q['question'],250)}",
            options=options,
            type="quiz",
            correct_option_id=q["correct"],
            is_anonymous=False
        )
    except Exception as e:
        print("Poll error:", e)

# =========================
# START
# =========================
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Xush kelibsiz!", reply_markup=main_menu())

@dp.message_handler(lambda m: m.text == "🚀 Test boshlash")
async def start_handler(message: types.Message):
    start_test(message.from_user)
    await message.answer("Boshladik 🔥", reply_markup=test_menu())
    await send_question(message.chat.id, message.from_user.id)

# =========================
# ANSWER
# =========================
@dp.poll_answer_handler()
async def poll_handler(poll_answer: types.PollAnswer):
    user_id = poll_answer.user.id

    data = users.get(user_id)
    if not data:
        return

    if data["index"] >= len(data["questions"]):
        return

    q = data["questions"][data["index"]]

    selected = poll_answer.option_ids[0]
    correct = q["correct"]

    subject = q["subject"]

    if subject not in data["subjects"]:
        data["subjects"][subject] = {"correct":0,"incorrect":0}

    if selected == correct:
        data["correct"] += 1
        data["subjects"][subject]["correct"] += 1
    else:
        data["incorrect"] += 1
        data["subjects"][subject]["incorrect"] += 1

    data["index"] += 1

    await send_question(user_id, user_id)

# =========================
# RESULT
# =========================
async def finish_test(chat_id, user_id):
    data = users.get(user_id)
    if not data:
        return

    total = data["correct"] + data["incorrect"]
    percent = (data["correct"]/total)*100 if total else 0

    total_time = int(time.time() - data["start_time"])
    m = total_time // 60
    s = total_time % 60

    text = f"🎯 NATIJA\n\n"
    text += f"👤 {data['fullname']}\n"
    text += f"✅ {data['correct']} ❌ {data['incorrect']} 📊 {percent:.1f}%\n"
    text += f"⏱ {m}m {s}s\n\n"

    for sub, st in data["subjects"].items():
        text += f"{sub} → ✅{st['correct']} ❌{st['incorrect']}\n"

    results.append({
        "fullname": data["fullname"],
        "username": data["username"],
        "correct": data["correct"],
        "incorrect": data["incorrect"],
        "percent": percent
    })

    save_db(results)

    await bot.send_message(chat_id, text, reply_markup=result_menu())

    users.pop(user_id, None)

# =========================
# STOP
# =========================
@dp.message_handler(lambda m: m.text == "🛑 Testni tugatish")
async def stop_test(message: types.Message):
    user_id = message.from_user.id

    if user_id not in users:
        return await message.answer("Test yo‘q")

    await message.answer("Test tugatildi 🛑")
    await finish_test(message.chat.id, user_id)

# =========================
# RESTART
# =========================
@dp.message_handler(lambda m: m.text == "🔁 Qaytadan boshlash")
async def restart(message: types.Message):
    start_test(message.from_user)

    user_id = message.from_user.id

    await message.answer("Qaytadan boshlandi 🔄", reply_markup=test_menu())
    await send_question(message.chat.id, user_id)

# =========================
# MENU
# =========================
@dp.message_handler(lambda m: m.text == "🏠 Menu")
async def menu(message: types.Message):
    users.pop(message.from_user.id, None)
    await message.answer("Menu", reply_markup=main_menu())

# =========================
# ADMIN
# =========================
@dp.message_handler(commands=["admin"])
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Admin emas")

    if not results:
        return await message.answer("Hali natija yo‘q")

    text = "👑 ADMIN PANEL\n\n"

    for i, u in enumerate(results, 1):
        text += f"{i}. {u.get('fullname')} (@{u.get('username')})\n"
        text += f"/user_{i}\n\n"

    await message.answer(text)

# =========================
# RUN
# =========================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
# import random
# import time
# from aiogram import Bot, Dispatcher, F
# from aiogram.enums import PollType
# from aiogram.filters import Command
# from aiogram.types import (
#     PollAnswer
# )
# from utils.database import *
# clear_fake_users()
#
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
# from aiogram.fsm.storage.memory import MemoryStorage
# import sys
# from docx import Document
# import asyncio
# if sys.platform.startswith("win"):
#     asyncio.set_event_loop_policy(
#         asyncio.WindowsSelectorEventLoopPolicy()
#     )
# import logging
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# TOKEN = os.getenv(
#     "BOT_TOKEN"
# )
# SUPER_ADMIN = int(
#     os.getenv(
#         "SUPER_ADMIN",
#         "0"
#     )
# )
# logging.basicConfig(level=logging.INFO)
#
# DATA_FOLDER = "data"
#
# QUESTIONS_PER_TEST = 20
#
# bot = Bot(TOKEN)
#
# dp = Dispatcher(storage=MemoryStorage())
#
# # ADMIN / USER SYSTEM
# # ============================
#
# from aiogram.types import (
#     Message,
#     ReplyKeyboardMarkup,
#     KeyboardButton
# )
#
# from aiogram import F
# from aiogram.fsm.state import (
#     State,
#     StatesGroup
# )
# from aiogram.fsm.context import FSMContext
#
#
# # =================
# # PERMISSION
# # =================
#
# def is_super(uid):
#
#     return uid == SUPER_ADMIN
#
# def is_admin(uid):
#
#     if uid == SUPER_ADMIN:
#
#         return True
#
#     return is_admin_db(uid)
#
#
# # =================
# # STATE
# # =================
#
# class AddAdmin(
#     StatesGroup
# ):
#     wait = State()
#
#
# class DelAdmin(
#     StatesGroup
# ):
#     wait = State()
#
#
# class AddUser(
#     StatesGroup
# ):
#     wait = State()
#
#
# class DelUser(
#     StatesGroup
# ):
#     wait = State()
#
#
# # =================
# # MENU
# # =================
# def main_menu(user_id):
#
#     kb = [
#
#         [
#             KeyboardButton(
#                 text="🚀 Testni boshlash"
#             )
#         ],
#
#         [
#             KeyboardButton(
#                 text="📊 Natijalar"
#             ),
#
#             KeyboardButton(
#                 text="🏆 Reyting"
#             )
#         ],
#
#         [
#             KeyboardButton(
#                 text="📚 Fanlar"
#             )
#         ]
#
#     ]
#
#     if is_admin(user_id):
#
#         kb.append(
#
#             [
#                 KeyboardButton(
#                     text="👑 Admin Panel"
#                 )
#             ]
#
#         )
#
#     return ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True
#     )
#
# def admin_menu():
#
#     kb = [
#
#         [
#             KeyboardButton(
#                 text="👥 Users"
#             ),
#
#             KeyboardButton(
#                 text="🛡 Admin"
#             )
#         ],
#
#         [
#             KeyboardButton(
#                 text="🏠 Home"
#             )
#         ]
#
#     ]
#
#     return ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True
#     )
#
# def users_menu():
#
#     kb = [
#
#         [
#             KeyboardButton(
#                 text="➕ User"
#             ),
#
#             KeyboardButton(
#                 text="❌ Del User"
#             )
#         ],
#
#         [
#             KeyboardButton(
#                 text="📋 User List"
#             )
#         ],
#
#         [
#             KeyboardButton(
#                 text="⬅ Back"
#             )
#         ]
#
#     ]
#
#     return ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True
#     )
#
# @dp.message(
#     F.text == "📋 User List"
# )
# async def users_list(
#         message: Message
# ):
#
#     users = get_users()
#
#     if len(users) == 0:
#
#         await message.answer(
#             "Bo‘sh"
#         )
#
#         return
#
#     text = "👥 USERS LIST\n\n"
#
#     for uid, fullname in users:
#
#         text += f"""
# 👤 {fullname}
#
# 🆔 {uid}
#
# ━━━━━━━━━━
# """
#
#     await message.answer(
#         text
#     )
# def admins_menu():
#
#     kb = [
#
#         [
#             KeyboardButton(
#                 text="➕ Admin"
#             ),
#
#             KeyboardButton(
#                 text="❌ Del Admin"
#             )
#         ],
#
#         [
#             KeyboardButton(
#                 text="📋 Admin List"
#             )
#         ],
#
#         [
#             KeyboardButton(
#                 text="⬅ Back"
#             )
#         ]
#
#     ]
#
#     return ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True
#     )
# @dp.message(
#     F.text == "📋 Admin List"
# )
# async def admin_list(
#         message: Message
# ):
#
#     text = "🛡 ADMINS\n\n"
#
#     text += (
#         f"👑 SUPER\n"
#         f"{SUPER_ADMIN}\n\n"
#     )
#
#     for uid in get_admins():
#
#         text += (
#             f"🆔 {uid}\n"
#         )
#
#         try:
#
#             chat = await bot.get_chat(
#                 uid
#             )
#
#             text += (
#                 f"👤 {chat.full_name}\n\n"
#             )
#
#         except:
#
#             text += (
#                 "👤 Noma'lum\n\n"
#             )
#
#     await message.answer(
#         text
#     )
#
# # =================
# # START
# # =================
# # =================
# # OPEN ADMIN
# # =================
#
# @dp.message(
#     F.text ==
#     "👑 Admin Panel"
# )
# async def open_admin(
#         message: Message
# ):
#
#     if not is_admin(
#             message.from_user.id
#     ):
#
#         await message.answer(
#             "❌ Ruxsat yo‘q"
#         )
#
#         return
#
#     await message.answer(
#         "👑 PANEL",
#         reply_markup=
#         admin_menu()
#     )
#
#
# # =================
# # USERS
# # =================
#
# @dp.message(
#     F.text ==
#     "👥 Users"
# )
# async def users_open(
#         message: Message
# ):
#
#     if not is_admin(
#             message.from_user.id
#     ):
#
#         return
#
#     await message.answer(
#         "👥 USERS",
#         reply_markup=
#         users_menu()
#     )
#
#
# # =================
# # ADMINS
# # =================
#
# @dp.message(
#     F.text ==
#     "🛡 Admin"
# )
# async def admins_open(
#         message: Message
# ):
#
#     if not is_super(
#             message.from_user.id
#     ):
#
#         await message.answer(
#             "❌ Faqat super admin"
#         )
#
#         return
#
#     await message.answer(
#         "🛡 ADMINS",
#         reply_markup=
#         admins_menu()
#     )
#
#
# # =================
# # ADD ADMIN
# # =================
#
# @dp.message(
#     F.text ==
#     "➕ Admin"
# )
# async def add_admin_open(
#         message: Message,
#         state: FSMContext
# ):
#
#     if not is_super(
#             message.from_user.id
#     ):
#
#         return
#
#     await state.set_state(
#         AddAdmin.wait
#     )
#
#     await message.answer(
#         "Admin ID"
#     )
#
# @dp.message(
#     AddAdmin.wait
# )
# async def save_admin(
#         message: Message,
#         state: FSMContext
# ):
#
#     if message.text == "⬅ Back":
#
#         await state.clear()
#
#         await message.answer(
#             "👑 ADMIN PANEL",
#             reply_markup=
#             admin_menu()
#         )
#
#         return
#
#     if not message.text.isdigit():
#
#         await message.answer(
#             "Faqat ID yuboring"
#         )
#
#         return
#
#     uid = int(
#         message.text
#     )
#
#     try:
#
#         chat = await bot.get_chat(
#             uid
#         )
#
#     except:
#
#         await message.answer(
# """
# User hali botga kirmagan
#
# 1. Botga kirsin
#
# 2. /start bossin
#
# 3. Keyin admin qiling
# """
#         )
#
#         return
#
#     if uid == SUPER_ADMIN:
#
#         await message.answer(
#             "⚠ Bu SUPER ADMIN",
#             reply_markup=
#             admin_menu()
#         )
#
#         await state.clear()
#
#         return
#
#     # ADMIN QO‘SHISH
#
#     add_admin_db(uid)
#
#     # REYTINGGA QO‘SHISH
#
#     save_result(
#         uid,
#         chat.full_name,
#         0,
#         0
#     )
#
#     await state.clear()
#
#     await message.answer(
# f"""
# ✅ Admin qo‘shildi
#
# 🆔 ID:
# {uid}
#
# 👤 {chat.full_name}
#
# 🏆 Reytingga ham qo‘shildi
# """,
#         reply_markup=
#         admin_menu()
#     )
# @dp.message(
#     F.text == "❌ Del Admin"
# )
# async def del_admin_start(
#         message: Message,
#         state: FSMContext
# ):
#
#     if not is_super(
#             message.from_user.id
#     ):
#
#         return
#
#     await state.set_state(
#         DelAdmin.wait
#     )
#
#     await message.answer(
#         "O‘chiriladigan Admin ID yuboring"
#     )
# # =================
# # DELETE ADMIN
# # =================
#
#
# @dp.message(
#     DelAdmin.wait
# )
# async def save_del_admin(
#         message: Message,
#         state: FSMContext
# ):
#
#     if message.text == "⬅ Back":
#
#         await state.clear()
#
#         await message.answer(
#             "🛡 ADMINS",
#             reply_markup=
#             admins_menu()
#         )
#
#         return
#
#     if not message.text.isdigit():
#
#         await message.answer(
#             "Faqat ID yuboring"
#         )
#
#         return
#
#     uid = int(
#         message.text
#     )
#
#     if uid == SUPER_ADMIN:
#
#         await message.answer(
#             "❌ SUPER ADMIN o‘chirilmaydi"
#         )
#
#         return
#
#     del_admin_db(uid)
#
#     await state.clear()
#
#     await message.answer(
# f"""
# 🗑 Admin o‘chirildi
#
# 🆔 {uid}
# """,
#         reply_markup=
#         admins_menu()
#     )
# # =================
#
# @dp.message(
#     F.text ==
#     "➕ User"
# )
# async def add_user_open(
#         message: Message,
#         state: FSMContext
# ):
#
#     if not is_admin(
#             message.from_user.id
#     ):
#
#         return
#
#     await state.set_state(
#         AddUser.wait
#     )
#
#     await message.answer(
#         "User ID"
#     )
#
# @dp.message(
#     AddUser.wait
# )
# async def save_user(
#         message: Message,
#         state: FSMContext
# ):
#
#     # BACK
#
#     if message.text == "⬅ Back":
#
#         await state.clear()
#
#         await message.answer(
#             "👥 USERS",
#             reply_markup=
#             users_menu()
#         )
#
#         return
#
#     # ID
#
#     if not message.text.isdigit():
#
#         await message.answer(
#             "ID kiriting"
#         )
#
#         return
#
#     uid = int(
#         message.text
#     )
#
#     # SUPER ADMIN
#
#     if uid == SUPER_ADMIN:
#
#         await message.answer(
#             "⚠ Bu SUPER ADMIN",
#             reply_markup=
#             users_menu()
#         )
#
#         await state.clear()
#
#         return
#
#     try:
#
#         chat = await bot.get_chat(
#             uid
#         )
#
#     except:
#
#         await message.answer(
# """
# User hali botga kirmagan
#
# 1. Botga kirsin
#
# 2. /start bossin
#
# 3. Keyin qo‘shing
# """
#         )
#
#         return
#
#     # USER BORLIGINI TEKSHIRISH
#
#     if is_user(uid):
#
#         await message.answer(
#             "⚠ User oldin qo‘shilgan"
#         )
#
#     else:
#
#         add_user_db(
#             uid,
#             chat.full_name
#         )
#         await message.answer(
# f"""
# ✅ User qo‘shildi
#
# 🆔 ID:
# {uid}
#
# 👤 {chat.full_name}
# """
#         )
#
#     await state.clear()
#
#     await message.answer(
#         "👥 USERS",
#         reply_markup=
#         users_menu()
#     )
# @dp.message(
#     F.text == "❌ Del User"
# )
# async def del_user_start(
#         message: Message,
#         state: FSMContext
# ):
#
#     if not is_admin(
#             message.from_user.id
#     ):
#
#         return
#
#     await state.set_state(
#         DelUser.wait
#     )
#
#     await message.answer(
#         "O‘chiriladigan ID yuboring"
#     )
# # =================
# # DELETE USER
# @dp.message(
#     DelUser.wait
# )
# async def save_del_user(
#         message: Message,
#         state: FSMContext
# ):
#
#     if message.text == "⬅ Back":
#
#         await state.clear()
#
#         await message.answer(
#             "👥 USERS",
#             reply_markup=
#             users_menu()
#         )
#
#         return
#
#     if not message.text.isdigit():
#
#         await message.answer(
#             "ID kiriting"
#         )
#
#         return
#
#     uid = int(
#         message.text
#     )
#
#     if uid == SUPER_ADMIN:
#
#         await message.answer(
#             "❌ SUPER ADMIN o‘chirib bo‘lmaydi"
#         )
#
#         return
#
#     if is_user(uid):
#
#         del_user_db(uid)
#
#         await message.answer(
# f"""
# 🗑 User o‘chirildi
#
# 🆔 {uid}
# """
#         )
#
#     else:
#
#         await message.answer(
#             "❌ User topilmadi"
#         )
#
#     await state.clear()
#
#     await message.answer(
#         "👥 USERS",
#         reply_markup=
#         users_menu()
#     )
# # =================
#
# @dp.message(
#     F.text == "⬅ Back"
# )
# async def back(
#         message: Message
# ):
#
#     uid = message.from_user.id
#
#     # SUPER ADMIN yoki ADMIN
#
#     if is_admin(
#             uid
#     ):
#
#         await message.answer(
#             "👑 PANEL",
#             reply_markup=
#             admin_menu()
#         )
#
#         return
#
#     # ODDIY USER
#
#     await message.answer(
#         "🏠 HOME",
#         reply_markup=
#         main_menu(
#             uid
#         )
#     )
#
#
# # =================
# # HOME
# # =================
#
# @dp.message(
#     F.text ==
#     "🏠 Home"
# )
# async def home(
#         message: Message
# ):
#
#     await message.answer(
#         "HOME",
#         reply_markup=
#         main_menu(
#             message.from_user.id
#         )
#     )
#
# # =====================================
# # TEST DATA
# # =====================================
#
# users_test = {}
#
# user_results = {}
#
# def clean_text(text):
#     return " ".join(str(text).split()).strip()
#
#
# # ==================================================
# # SAVE / LOAD LEADERBOARD
#
# # =========================================
# # LOAD QUESTIONS
# # =========================================
#
# def load_questions():
#     questions = []
#
#     for filename in os.listdir(DATA_FOLDER):
#
#         if filename.startswith("~$"):
#             continue
#
#         if not filename.endswith(".docx"):
#             continue
#
#         path = os.path.join(DATA_FOLDER, filename)
#
#         print(f"Yuklanmoqda: {filename}")
#
#         try:
#
#             doc = Document(path)
#
#             # =====================================
#             # TABLE O'QISH
#             # =====================================
#
#             for table in doc.tables:
#
#                 for row in table.rows:
#
#                     try:
#
#                         cells = row.cells
#
#                         # normal row
#                         if len(cells) < 5:
#                             continue
#
#                         texts = []
#
#                         for cell in cells:
#
#                             txt = " ".join(
#                                 clean_text(p.text)
#                                 for p in cell.paragraphs
#                                 if clean_text(p.text)
#                             )
#
#                             txt = clean_text(txt)
#
#                             if txt:
#                                 texts.append(txt)
#
#                         # minimum 5 ta ustun
#                         if len(texts) < 5:
#                             continue
#
#                         # =====================================
#                         # SAVOL
#                         # =====================================
#
#                         question = clean_text(texts[0])
#
#                         if not question:
#                             continue
#
#                         # HEADER FILTER
#                         # HEADERLARNI FILTER QILISH
#                         bad_headers = [
#                             "test savoli",
#                             "to‘g‘ri javob",
#                             "muqobil javob",
#                             "universitet",
#                             "business and science",
#                             "o‘quv yili",
#                             "ta’lim yo‘nalishi",
#                             "yakuniy davlat attestatsiyasi",
#                         ]
#
#                         q_lower = question.lower()
#
#                         # faqat headerlarni skip qil
#                         if any(x in q_lower for x in bad_headers):
#                             continue
#
#                         # juda qisqa bo‘lsa skip
#                         if len(question.strip()) < 3:
#                             continue
#
#                         # =====================================
#                         # JAVOBLAR
#                         # =====================================
#
#                         answers = []
#
#                         for ans in texts[1:5]:
#
#                             ans = clean_text(ans)
#
#                             if not ans:
#                                 ans = "Variant mavjud emas"
#
#                             # Telegram limit
#                             ans = ans[:95]
#
#                             answers.append(ans)
#
#                         # duplicate variantlarni olib tashlash
#                         answers = list(dict.fromkeys(answers))
#
#                         # minimum 2 ta javob
#                         if len(answers) < 2:
#                             continue
#
#                         # 4 tagacha to'ldirish
#                         while len(answers) < 4:
#                             answers.append("Variant mavjud emas")
#
#                         answers = answers[:4]
#
#                         # =====================================
#                         # SAVE
#                         # =====================================
#
#                         questions.append({
#                             "subject": filename.replace(".docx", ""),
#                             "question": question[:300],
#                             "correct": answers[0],
#                             "answers": answers
#                         })
#
#                     except Exception as e:
#                         print("TABLE ERROR:", e)
#
#         except Exception as e:
#
#             print("XATO:", filename)
#             print(e)
#
#     print(f"JAMI SAVOLLAR: {len(questions)}")
#
#     return questions
#
#
# ALL_QUESTIONS = load_questions()
#
#
#
# # ==================================================
# # START
# # ==================================================
# # ==================================================
# # START
# # ==================================================
#
# # ==================================================
# # START
# # ==================================================
#
# @dp.message(
#     Command("start")
# )
# async def start(
#         message: Message
# ):
#
#     uid = message.from_user.id
#
#     # ==========================
#     # RUXSAT
#     # ==========================
#
#     if (
#         uid != SUPER_ADMIN
#         and not is_admin_db(uid)
#         and not is_user(uid)
#     ):
#
#         await message.answer(
# """
# ⛔ Sizga ruxsat yo‘q
#
# Botdan foydalanish uchun:
#
# 📩 @dasturchi_0101 ga murojaat qiling
#
# Admin sizni qo‘shgandan keyin foydalanasiz.
# """
#         )
#
#         return
#
#     # ==========================
#     # SUPER ADMIN
#     # ==========================
#
#     if uid == SUPER_ADMIN:
#
#         text = f"""
# 👑 <b>SUPER ADMIN PANEL</b>
#
# ━━━━━━━━━━━━━━━━━━
#
# 📚 <b>Test bazasi</b>
#
# 📝 Savollar:
# <b>{len(ALL_QUESTIONS)}</b>
#
# 👥 Users:
# <b>{len(get_users())}</b>
#
# 🛡 Adminlar:
# <b>{len(get_admins())}</b>
#
# ━━━━━━━━━━━━━━━━━━
#
# ⚙ Imkoniyatlar
#
# ➕ User qo‘shish
#
# ❌ User o‘chirish
#
# 🛡 Admin boshqaruvi
#
# 🏆 Reyting
#
# 📊 Statistika
#
# 📚 Fanlar
#
# ━━━━━━━━━━━━━━━━━━
#
# 🚀 Tizim tayyor
# """
#
#         await message.answer(
#             text,
#             parse_mode="HTML",
#             reply_markup=
#             main_menu(uid)
#         )
#
#         return
#
#     # ==========================
#     # ADMIN
#     # ==========================
#
#     if is_admin_db(uid):
#
#         text = f"""
# 👑 <b>ADMIN PANEL</b>
#
# ━━━━━━━━━━━━━━━━━━
#
# 📚 <b>Test bazasi</b>
#
# 📝 Savollar:
# <b>{len(ALL_QUESTIONS)}</b>
#
# 👥 Users:
# <b>{len(get_users())}</b>
#
# 🛡 Adminlar:
# <b>{len(get_admins())}</b>
#
# ━━━━━━━━━━━━━━━━━━
#
# ⚙ Boshqaruv
#
# ➕ User qo‘shish
#
# ❌ User o‘chirish
#
# 🏆 Reyting
#
# 📊 Statistika
#
# 📚 Fanlar
#
# ━━━━━━━━━━━━━━━━━━
#
# 🚀 Bot ishga tayyor
# """
#
#         await message.answer(
#             text,
#             parse_mode="HTML",
#             reply_markup=
#             main_menu(uid)
#         )
#
#         return
#
#     # ==========================
#     # USER
#     # ==========================
#
#     text = f"""
# 🎓 <b>QUIZ BOT</b>
#
# ━━━━━━━━━━━━━━━━━━
#
# 📚 Savollar:
# <b>{len(ALL_QUESTIONS)}</b>
#
# 🏆 Reyting
#
# 📊 Natijalar
#
# 📘 Fanlar bo‘yicha test
#
# 🌍 Umumiy test
#
# ━━━━━━━━━━━━━━━━━━
#
# ✅ Assalomu alaykum
#
# Quiz botga xush kelibsiz
#
# 🚀 Testni boshlash tugmasini bosing
# """
#
#     await message.answer(
#         text,
#         parse_mode="HTML",
#         reply_markup=
#         main_menu(uid)
#     )
#
#
#
# # ==================================================
# # TEST MENU
# # ==================================================
# @dp.message(
#     F.text == "🚀 Testni boshlash"
# )
# async def test_menu(
#         message: Message
# ):
#
#     uid = message.from_user.id
#
#     # RUXSAT TEKSHIRISH
#
#     if (
#             uid != SUPER_ADMIN
#             and not is_admin_db(uid)
#             and not is_user(uid)
#     ):
#
#
#         await message.answer(
# """
# ⛔ Sizga ruxsat berilmagan
#
# Botdan foydalanish uchun:
#
# 📩 @dasturchi_0101 ga murojaat qiling
#
# Admin sizni qo‘shgandan keyin test ishlaydi.
# """
#         )
#
#         return
#
#     counts = {}
#
#     for q in ALL_QUESTIONS:
#
#         subject = q[
#             "subject"
#         ]
#
#         counts[
#             subject
#         ] = counts.get(
#             subject,
#             0
#         ) + 1
#
#     text = (
#         "📚 Qaysi fandan test ishlaysiz?\n\n"
#     )
#
#     kb = ReplyKeyboardBuilder()
#
#     total = 0
#
#     for subject, count in counts.items():
#
#         total += count
#
#         text += (
#             f"📘 {subject}"
#             f" — {count} ta savol\n"
#         )
#
#         kb.row(
#
#             KeyboardButton(
#                 text=
#                 f"📘 {subject}"
#             )
#
#         )
#
#     text += (
#         f"\n🌍 Barcha fanlar"
#         f" — {total} ta savol"
#     )
#
#     kb.row(
#
#         KeyboardButton(
#             text=
#             "🌍 Barcha fanlar"
#         )
#
#     )
#
#     kb.row(
#
#         KeyboardButton(
#             text=
#             "🛑 Testni tugatish"
#         )
#
#     )
#
#     await message.answer(
#         text,
#         reply_markup=
#         kb.as_markup(
#             resize_keyboard=True
#         )
#     )
#
#
# # ==================================================
# # SUBJECT TEST
# # ==================================================
#
# @dp.message(F.text.startswith("📘 "))
# async def subject_test(message: Message):
#     user_id = message.from_user.id
#
#     subject_name = (
#         message.text
#         .replace("📘 ", "")
#         .split(" — ")[0]
#     )
#
#     questions = [
#         q for q in ALL_QUESTIONS
#         if q["subject"] == subject_name
#     ]
#
#     if not questions:
#         await message.answer(
#             "❌ Savollar topilmadi"
#         )
#         return
#
#     random.shuffle(questions)
#
#     questions = questions[:QUESTIONS_PER_TEST]
#
#     users_test[user_id] = {
#         "questions": questions,
#         "index": 0,
#         "correct": 0,
#         "wrong": 0,
#         "skipped": 0,
#         "chat_id": message.chat.id,
#         "start_time": time.time(),
#         "answered": False,
#         "subjects": {},
#         "full_name": message.from_user.full_name
#
#     }
#
#     await send_question(user_id)
#
#
# # ==================================================
# # ALL SUBJECTS TEST
# # ==================================================
#
# @dp.message(F.text == "🌍 Barcha fanlar")
# async def all_subjects_test(message: Message):
#     user_id = message.from_user.id
#
#     questions = ALL_QUESTIONS.copy()
#
#     random.shuffle(questions)
#
#     questions = questions[:QUESTIONS_PER_TEST]
#
#     users_test[user_id] = {
#         "questions": questions,
#         "index": 0,
#         "correct": 0,
#         "wrong": 0,
#         "skipped": 0,
#         "chat_id": message.chat.id,
#         "start_time": time.time(),
#         "answered": False,
#         "subjects": {},
#         "full_name": message.from_user.full_name
#     }
#
#     await send_question(user_id)
#
#
# async def send_question(user_id):
#     if user_id not in users_test:
#         return
#
#     data = users_test[user_id]
#
#     if data["index"] >= len(data["questions"]):
#
#         total = (
#                 data["correct"] +
#                 data["wrong"] +
#                 data["skipped"]
#         )
#
#         correct = data["correct"]
#
#         percent = round(
#             (correct / total) * 100,
#             1
#         ) if total > 0 else 0
#
#         spent = int(
#             time.time() - data["start_time"]
#         )
#
#         # FANLAR BO'YICHA
#         # =====================================
#
#         subjects_text = "\n📚 Fanlar bo'yicha:\n\n"
#
#         for sub, stat in data["subjects"].items():
#             subjects_text += (
#                 f"📘 {sub}\n"
#                 f"✅ {stat['correct']} | "
#                 f"❌ {stat['wrong']} | "
#                 f"⏭ {stat['skipped']}\n\n"
#             )
#
#         # =====================================
#         # RESULT TEXT
#
#         result_text = f"""
#         😔 TEST NATIJALARI
#
#         👤 User ID: {user_id}
#
#         📊 Jami savol: {total}
#
#         ✅ To'g'ri: {data['correct']}
#         ❌ Noto'g'ri: {data['wrong']}
#         ⏭ O'tkazilgan: {data['skipped']}
#
#         🎯 Ball: {percent}%
#
#         ⏱ Vaqt:
#         {spent // 60} daq {spent % 60} son
#
#         {subjects_text}
#         """
#
#         # =====================================
#         # RESULT SAVE
#         # =====================================
#
#         user_results[user_id] = result_text
#
#         # =====================================
#         # GLOBAL REYTING
#         # =====================================
#
#         save_result(
#             user_id,
#             data["full_name"],
#             data["correct"],
#             total
#         )
#
#         await bot.send_message(
#             data["chat_id"],
#             result_text,
#             reply_markup=main_menu(user_id)
#         )
#
#         del users_test[user_id]
#
#         return
#
#     q = data["questions"][data["index"]]
#
#     answers = []
#
#     for a in q["answers"]:
#
#         a = clean_text(a)
#
#         if len(a) > 90:
#             a = a[:90]
#
#         answers.append(a)
#
#     answers = list(dict.fromkeys(answers))
#
#     if len(answers) < 2:
#         data["index"] += 1
#
#         await send_question(user_id)
#
#         return
#
#     correct_answer = clean_text(q["correct"])
#
#     if len(correct_answer) > 90:
#         correct_answer = correct_answer[:90]
#
#     if correct_answer not in answers:
#         answers[0] = correct_answer
#
#     random.shuffle(answers)
#
#     correct_index = answers.index(correct_answer)
#
#     data["correct_index"] = correct_index
#     data["answered"] = False
#
#     text = (
#         f"📝 {data['index'] + 1}/{len(data['questions'])} | "
#         f"🚀 {q['subject']}\n\n"
#         f"{q['question'][:250]}"
#     )
#
#     await bot.send_poll(
#         chat_id=data["chat_id"],
#         question=text[:300],
#         options=answers[:4],
#         type=PollType.QUIZ,
#         correct_option_id=correct_index,
#         is_anonymous=False,
#         # open_period=25,# timer ochirish
#         explanation=f"✅ To'g'ri: {correct_answer}"
#     )
#
#
# # ==================================================
# # POLL ANSWER
# # ==================================================
#
# @dp.poll_answer()
# async def poll_answer_handler(
#         poll_answer: PollAnswer
# ):
#     user_id = poll_answer.user.id
#
#     if user_id not in users_test:
#         return
#
#     data = users_test[user_id]
#
#     if data["answered"]:
#         return
#
#     data["answered"] = True
#
#     # =====================================
#     # CURRENT QUESTION
#     # =====================================
#
#     q = data["questions"][data["index"]]
#
#     subject = q["subject"]
#
#     # subject stat yaratish
#     if subject not in data["subjects"]:
#         data["subjects"][subject] = {
#             "correct": 0,
#             "wrong": 0,
#             "skipped": 0
#         }
#
#     # =====================================
#     # SKIPPED
#     # =====================================
#
#     if not poll_answer.option_ids:
#
#         data["skipped"] += 1
#
#         data["subjects"][subject]["skipped"] += 1
#
#     else:
#
#         selected = poll_answer.option_ids[0]
#
#         # =================================
#         # TO'G'RI
#         # =================================
#
#         if selected == data["correct_index"]:
#
#             data["correct"] += 1
#
#             data["subjects"][subject]["correct"] += 1
#
#         # =================================
#         # NOTO'G'RI
#         # =================================
#
#         else:
#
#             data["wrong"] += 1
#
#             data["subjects"][subject]["wrong"] += 1
#
#     # =====================================
#     # NEXT QUESTION
#     # =====================================
#
#     data["index"] += 1
#
#     await asyncio.sleep(2)
#
#     await send_question(user_id)
#
#
# # ==================================================
# # RESULTS
# # ==================================================
# @dp.message(
#     F.text == "📊 Natijalar"
# )
# async def results(
#         message: Message
# ):
#
#     uid = message.from_user.id
#
#     if (
#             uid != SUPER_ADMIN
#             and not is_admin_db(uid)
#             and not is_user(uid)
#     ):
#
#         await message.answer(
# """
# ⛔ Sizda ruxsat yo‘q
# """
#         )
#
#         return
#
#     if uid not in user_results:
#
#         await message.answer(
#             "❌ Natija yo‘q"
#         )
#
#         return
#
#     await message.answer(
#         user_results[uid]
#     )
#
#
# # ==================================================
# # GLOBAL REYTING
# # ==================================================
# @dp.message(
#     F.text == "🏆 Reyting"
# )
# async def leaderboard(
#         message: Message
# ):
#
#     uid = message.from_user.id
#
#     if (
#             uid != SUPER_ADMIN
#             and not is_admin_db(uid)
#             and not is_user(uid)
#     ):
#
#         await message.answer(
# """
# ⛔ Reytingni ko‘rishga ruxsat yo‘q
# """
#         )
#
#         return
#
#     board = get_leaderboard()
#
#     if len(board) == 0:
#
#         await message.answer(
#             "❌ Reyting bo‘sh"
#         )
#
#         return
#
#     text = "🏆 GLOBAL REYTING\n\n"
#
#     for i, row in enumerate(
#             board,
#             start=1
#     ):
#
#         name = row[0]
#
#         correct = row[1]
#
#         total = row[2]
#
#         percent = round(
#             (
#                 correct /
#                 total
#             ) * 100,
#             1
#         ) if total else 0
#
#         mark = ""
#
#         # O‘ZINI BELGILASH
#
#         if uid == SUPER_ADMIN:
#
#             if name == message.from_user.full_name:
#                 mark = " ⭐"
#
#         else:
#
#             if name == message.from_user.full_name:
#                 mark = " ⭐"
#
#         text += (
#             f"{i}. 👤 {name}{mark}\n"
#             f"✅ {correct}/{total}\n"
#             f"🎯 {percent}%\n\n"
#         )
#
#     await message.answer(
#         text
#     )
# # ==================================================
# # FANLAR
# # ==================================================
#
# @dp.message(F.text == "📚 Fanlar")
# async def subjects(message: Message):
#     counts = {}
#
#     total = 0
#
#     for q in ALL_QUESTIONS:
#         counts[q["subject"]] = (
#                 counts.get(q["subject"], 0) + 1
#         )
#
#         total += 1
#
#     text = "📚 MAVJUD FANLAR\n\n"
#
#     for subject, count in counts.items():
#         text += f"📘 {subject} — {count} ta savol\n"
#
#     text += f"\n📝 Jami: {total} ta test"
#
#     await message.answer(text)
#
#
# # ==================================================
# # STOP TEST
# # ==================================================
#
#
# # ==================================================
# # TESTNI TUGATISH
# # ==================================================
#
# @dp.message(F.text == "🛑 Testni tugatish")
# async def stop_test(message: Message):
#     user_id = message.from_user.id
#
#     # test boshlanmagan
#     if user_id not in users_test:
#         await message.answer(
#             "❌ Siz hali test boshlamagansiz",
#             reply_markup=main_menu(message.from_user.id)
#         )
#         return
#
#     data = users_test[user_id]
#
#     total = (
#             data["correct"] +
#             data["wrong"] +
#             data["skipped"]
#     )
#
#     # hech narsa ishlamagan
#     if total == 0:
#         await message.answer(
#             "❌ Siz hali savol ishlamagansiz",
#             reply_markup=main_menu(message.from_user.id)
#         )
#         return
#
#     # =====================================
#     # BALL
#     # =====================================
#
#     percent = round(
#         (data["correct"] / total) * 100,
#         1
#     )
#
#     spent = int(
#         time.time() - data["start_time"]
#     )
#
#     # =====================================
#     # FANLAR
#     # =====================================
#
#     subjects_text = "\n📚 Fanlar bo'yicha:\n\n"
#
#     for sub, stat in data["subjects"].items():
#         subjects_text += (
#             f"📘 {sub}\n"
#             f"✅ {stat['correct']} | "
#             f"❌ {stat['wrong']} | "
#             f"⏭ {stat['skipped']}\n\n"
#         )
#
#     # =====================================
#     # RESULT
#     # =====================================
#
#     result_text = f"""
# 😔 TEST NATIJALARI
#
# 👤 User ID: {user_id}
#
# 📊 Jami savol: {total}
#
# ✅ To'g'ri: {data['correct']}
# ❌ Noto'g'ri: {data['wrong']}
# ⏭ O'tkazilgan: {data['skipped']}
#
# 🎯 Ball: {percent}%
#
# ⏱ Vaqt:
# {spent // 60} daq {spent % 60} son
#
# {subjects_text}
# """
#
#     # saqlash
#     user_results[user_id] = result_text
#
#     # =====================================
#     # GLOBAL REYTING
#     # =====================================
#
#     save_result(
#         user_id,
#         message.from_user.full_name,
#         data["correct"],
#         total
#     )
#
#     await message.answer(
#         result_text,
#         reply_markup=main_menu(message.from_user.id)
#     )
#
#     # testni yopish
#     del users_test[user_id]
#
#
# # =========================================
# # MAIN
# # =========================================
#
# async def main():
#     while True:
#
#         try:
#
#             print("BOT ISHGA TUSHDI")
#             print("SAVOLLAR:", len(ALL_QUESTIONS))
#
#             await dp.start_polling(bot)
#
#         except Exception as e:
#
#             print("XATO:", e)
#             print("5 sekunddan keyin qayta ulanadi...")
#
#             await asyncio.sleep(5)
#
#
# # =========================================
# # START
# # =========================================
#
# if __name__ == "__main__":
#
#     try:
#         asyncio.run(main())
#
#     except KeyboardInterrupt:
#         print("Dastur yopildi")
#



















import sqlite3
from aiogram import Router, types, F
from aiogram.types import Message
from keyboards import reply, inline

router = Router()
con = sqlite3.connect("database.db")
cur = con.cursor()

@router.message(F.text == "/start")
async def command_start_handler(message: Message):
    if not cur.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,)).fetchone():
        cur.execute("INSERT INTO users(id) VALUES (?)", (message.from_user.id,))
        con.commit()
    await message.answer(f"Привіт, {message.from_user.full_name}!",reply_markup=reply.main_mk)

@router.message(F.text == "🛒 Каталог товарів")
async def category_list(message: types.Message):
    await message.answer("Виберіть потрібну <b>категорію:</b>", reply_markup=inline.smart_builder(type="category", action="user_category"))

@router.message(F.text == "🔎 Пошук")
async def category_list(message: types.Message):
    await message.answer("Пошук")

@router.message(F.text == "🤵 Особистий кабінет")
async def help(message: types.Message):
    await message.answer("Особистий кабінет")

@router.message(F.text == "⁉️ Допомога")
async def help(message: types.Message):
    await message.answer("Допомога")
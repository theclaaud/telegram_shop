import sqlite3
import os
from dotenv import load_dotenv
from aiogram import Router, types, F
from aiogram.types import Message
from keyboards import reply, inline

load_dotenv(".env")
router = Router()
ADMIN_ID = int(os.getenv("ADMIN_ID"))
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
    await message.answer("Каталог товарів")

@router.message(F.text == "🔎 Пошук")
async def category_list(message: types.Message):
    await message.answer("Пошук")

@router.message(F.text == "👨 Особистий кабінет")
async def help(message: types.Message):
    await message.answer("Особистий кабінет")

@router.message(F.text == "⁉️ Допомога")
async def help(message: types.Message):
    await message.answer("Допомога")

@router.message(F.text == "/admin")
async def help(message: types.Message):
    if message.from_user.id == ADMIN_ID or cur.execute("SELECT is_admin FROM users WHERE id = ?", (message.from_user.id,)).fetchone()[0] == 1:
        await message.answer("👑 Адмін панель",reply_markup=inline.admin_mk)
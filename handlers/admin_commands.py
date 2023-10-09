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

@router.message(F.text == "/admin")
async def admin(message: types.Message):
    if message.from_user.id == ADMIN_ID or cur.execute("SELECT is_admin FROM users WHERE id = ?", (message.from_user.id,)).fetchone()[0] == 1:
        await message.answer("👑 Адмін панель",reply_markup=inline.admin_mk)
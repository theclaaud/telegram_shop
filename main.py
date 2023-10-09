import asyncio
import logging
import sys
import sqlite3
import markups
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

load_dotenv(".env")
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
con = sqlite3.connect("database.db")
cur = con.cursor()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    if not cur.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,)).fetchone():
        cur.execute("INSERT INTO users(id) VALUES (?)", (message.from_user.id,))
        con.commit()
    await message.answer(f"Привіт, {hbold(message.from_user.full_name)}!",reply_markup=markups.main_mk)


# сначала категория
# потом сам товар
# потом можно купить посмотреть и тд

@dp.message(F.text == "🛒 Каталог товарів")
async def category_list(message: types.Message):
    # if message.cha
    await message.answer("Каталог товарів")

@dp.message(F.text == "🔎 Пошук")
async def category_list(message: types.Message):
    await message.answer("Пошук")

@dp.message(F.text == "👨 Особистий кабінет")
async def help(message: types.Message):
    await message.answer("Особистий кабінет")

@dp.message(F.text == "⁉️ Допомога")
async def help(message: types.Message):
    await message.answer("Допомога")

@dp.message(F.text == "/admin")
async def help(message: types.Message):
    if message.from_user.id == ADMIN_ID or cur.execute("SELECT is_admin FROM users WHERE id = ?", (message.from_user.id,)).fetchone()[0] == 1:
        await message.answer("👑 Адмін панель",reply_markup=markups.admin_mk)

async def main():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id           INTEGER PRIMARY KEY
                         NOT NULL
                         UNIQUE,
    balance      INTEGER DEFAULT (0),
    phone_number TEXT,
    is_admin     BOOLEAN DEFAULT (0)
);
""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id    INTEGER PRIMARY KEY AUTOINCREMENT
                    NOT NULL,
        title TEXT    UNIQUE
                    NOT NULL
    );
""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS lots (
        id       INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL,
        title    TEXT    NOT NULL,
        price    INTEGER NOT NULL,
        category TEXT    NOT NULL
                        REFERENCES categories (title) ON UPDATE CASCADE
    );
""")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from handlers import user_commands, admin_commands
from callbacks import admin_callbacks
from data import create_db

load_dotenv(".env")
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

async def main():
    dp = Dispatcher()
    dp.include_routers(
        user_commands.router,
        admin_commands.router,
    )
    dp.callback_query.register(admin_callbacks.admin, F.data.startwith("adm"))

    create_db.create()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
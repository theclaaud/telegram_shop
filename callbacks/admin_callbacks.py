from aiogram import Bot
from aiogram.types import CallbackQuery

async def admin(call: CallbackQuery, bot: Bot):
    data = call.data
    await call.message.answer("clicked")
    await call.answer()
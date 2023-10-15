from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import AdminHandler, setup_cut_mk, admin_mk

router = Router()

@router.callback_query(AdminHandler.filter(F.value == "category"))
async def setup_categories(query: CallbackQuery, callback_data: AdminHandler):
    if callback_data.action == "add":
        await query.message.edit_text("add")
        await query.answer()
    elif callback_data.action == "remove":
        await query.message.edit_text("remove")
        await query.answer()
    elif callback_data.action == "list":
        await query.message.edit_text("list")
        await query.answer()
    else:
        await query.message.edit_text("Виберіть дію:",reply_markup=setup_cut_mk)
        await query.answer()

@router.callback_query(AdminHandler.filter(F.value == "lots"))
async def setup_lots(query: CallbackQuery, callback_data: AdminHandler):
    await query.message.answer("lots")
    await query.answer()

@router.callback_query(AdminHandler.filter(F.value == "users"))
async def setup_users(query: CallbackQuery, callback_data: AdminHandler):
    await query.message.answer("users")
    await query.answer()

@router.callback_query(AdminHandler.filter(F.value == "back"))
async def back(query: CallbackQuery, callback_data: AdminHandler):
    await query.message.edit_text("👑 Адмін панель",reply_markup=admin_mk)
    await query.answer()
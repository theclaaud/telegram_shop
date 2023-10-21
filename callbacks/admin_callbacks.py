import sqlite3
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from utils.states import AddCategory
from keyboards.inline import AdminHandler, RemoveItems, setup_cut_mk, admin_mk, setup_lot_mk, clear_state_mk, back_mk, remove_category_mk, categories_list_mk

router = Router()
con = sqlite3.connect("database.db")
cur = con.cursor()

@router.callback_query(AdminHandler.filter(F.value == "category"))
async def setup_categories(query: CallbackQuery, callback_data: AdminHandler, state: FSMContext):
    if callback_data.action == "add":
        await state.set_state(AddCategory.title)
        await query.message.answer("➕ Введіть назву категорії:",reply_markup=clear_state_mk)
        await query.answer()
    elif callback_data.action == "remove":
        await query.message.edit_text("Виберіть яку категорію видалити:", reply_markup=remove_category_mk())
    elif callback_data.action == "list":
        await query.message.edit_text("Список категорій:", reply_markup=categories_list_mk())
    else:
        await query.message.edit_text("Виберіть дію:",reply_markup=setup_cut_mk)

@router.message(AddCategory.title)
async def add_category(message: Message, state: FSMContext):
    cur.execute("INSERT INTO categories (title) VALUES (?)", (message.text,))
    con.commit()
    await message.answer(f"Категорію <b>{message.text}</b> додано!")
    await state.clear()    

@router.callback_query(RemoveItems.filter(F.type == "category"))
async def remove_category(query: CallbackQuery, callback_data: AdminHandler):
    remove_id = callback_data.id
    cur.execute("DELETE FROM categories WHERE id = ?", (remove_id,))
    con.commit()
    await query.message.edit_text("✅ Категорія видалена",reply_markup=back_mk)

@router.callback_query(AdminHandler.filter(F.value == "lots"))
async def setup_lots(query: CallbackQuery, callback_data: AdminHandler):
    if callback_data.action == "add":
        await query.message.edit_text("add")
    elif callback_data.action == "remove":
        await query.message.edit_text("remove")
    elif callback_data.action == "list":
        await query.message.edit_text("list")
    else:
        await query.message.edit_text("Виберіть дію:",reply_markup=setup_lot_mk)

@router.callback_query(AdminHandler.filter(F.value == "users"))
async def setup_users(query: CallbackQuery, callback_data: AdminHandler):
    await query.message.edit_text("Введіть id користувача:") # тут фсм типо будет
    await query.answer()

@router.callback_query(AdminHandler.filter(F.value == "clear_state"))
async def clear_state(query: CallbackQuery, callback_data: AdminHandler, state: FSMContext):
    await state.clear()
    await query.message.edit_text("Скасовано")
    await query.answer()

@router.callback_query(AdminHandler.filter(F.value == "category_click"))
async def category_click(query: CallbackQuery, callback_data: AdminHandler):
    await query.answer()

@router.callback_query(AdminHandler.filter(F.value == "back"))
async def back(query: CallbackQuery, callback_data: AdminHandler):
    await query.message.edit_text("👑 Адмін панель",reply_markup=admin_mk)
    await query.answer()
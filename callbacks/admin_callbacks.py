import sqlite3
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from utils.states import AddCategory, AddLot
from keyboards.inline import (AdminHandler, RemoveItems,
                              setup_cut_mk, admin_mk ,setup_lot_mk,clear_state_mk, back_mk,
                              smart_builder)

router = Router()
con = sqlite3.connect("database.db")
cur = con.cursor()

@router.callback_query(AdminHandler.filter(F.value == "category"))
async def setup_categories(query: CallbackQuery, callback_data: AdminHandler, state: FSMContext):
    if callback_data.action == "add":
        await state.set_state(AddCategory.title)
        await query.message.answer("➕ Введіть назву категорії:", reply_markup=clear_state_mk)
        await query.answer()
    elif callback_data.action == "remove":
        await query.message.edit_text("Виберіть яку категорію видалити:", reply_markup=smart_builder(type="category", action="remove", back_type=1))
    elif callback_data.action == "list":
        await query.message.edit_text("Список категорій:", reply_markup=smart_builder(type="category", action="list", back_type=1))
    else:
        await query.message.edit_text("Виберіть дію:", reply_markup=setup_cut_mk)

@router.message(AddCategory.title)
async def add_category(message: Message, state: FSMContext):
    cur.execute("INSERT INTO categories (title) VALUES (?)", (message.text,))
    con.commit()
    await message.answer(f"Категорію <b>{message.text}</b> додано!", reply_markup=back_mk)
    await state.clear()

@router.callback_query(RemoveItems.filter(F.type == "category"))
async def remove_category(query: CallbackQuery, callback_data: AdminHandler):
    remove_id = callback_data.id
    cur.execute("DELETE FROM categories WHERE id = ?", (remove_id,))
    con.commit()
    await query.message.edit_text("✅ Категорія видалена", reply_markup=back_mk)

@router.callback_query(AdminHandler.filter(F.value == "lots"))
async def setup_lots(query: CallbackQuery, callback_data: AdminHandler, state: FSMContext):
    if callback_data.action == "add":
        await state.set_state(AddLot.title)
        await query.message.answer("➕ Введіть <b>назву</b> товару:", reply_markup=clear_state_mk)
        await query.answer()
    elif callback_data.action == "remove":
        await query.message.edit_text("Виберіть <b>категрію</b>, в якій знаходиться <b>товар</b>, який потрібно <b>видалити</b>",reply_markup=smart_builder(type="category", action="select_cat_for_remove_lot", back_type=1))
    elif callback_data.action == "list":
        await query.message.edit_text("Список товарів:",reply_markup=smart_builder(type="lot", action="list", back_type=1))
    else:
        await query.message.edit_text("Виберіть дію:", reply_markup=setup_lot_mk)

@router.message(AddLot.title)
async def add_lot_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddLot.price)
    await message.answer("Добре, тепер введіть <b>ціну</b> товару")

@router.message(AddLot.price)
async def add_lot_price(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price=message.text)
        await state.set_state(AddLot.category)
        await message.answer("Добре, тепер виберіть <b>категорію</b> товару", reply_markup=smart_builder(type="category", action="add_lot_category", back_type=1))
    else:
        await message.answer("Введіть число!")

@router.callback_query(AdminHandler.filter(F.value == "add_lot_category"))
async def add_lot_category(query: CallbackQuery, callback_data: AdminHandler, state: FSMContext):
    await state.update_data(category = callback_data.action)
    await query.message.edit_text("Відправте фото товару:")

    await state.set_state(AddLot.image)

@router.message(AddLot.image, F.photo)
async def add_lot_image(message: Message, state: FSMContext):
    await state.update_data(image = message.photo[-1].file_id)
    items = await state.get_data()
    cur.execute("INSERT INTO lots (title, price, image_id, category) VALUES (?, ?, ?, ?)", (items["title"], items["price"], items["image"], items["category"]))
    con.commit()

    await message.answer_photo(photo=message.photo[-1].file_id, caption="\n".join([f"{key}: {item}" for key, item in (await state.get_data()).items()]))
    await state.clear()

@router.callback_query(AdminHandler.filter(F.value == "select_cat_for_remove_lot"))
async def enter_lot_remove(query: CallbackQuery, callback_data: AdminHandler):
    await query.message.edit_text("Добре, тепер <b>виберіть товар</b> який потрібно <b>видалити</b>",reply_markup=smart_builder(type="lot_with_cat", action="remove", id=callback_data.action, back_type=1))

@router.callback_query(RemoveItems.filter(F.type == "lot_with_cat"))
async def remove_lot(query: CallbackQuery, callback_data: AdminHandler):
    remove_id = callback_data.id
    cur.execute("DELETE FROM lots WHERE id = ?", (remove_id,))
    con.commit()
    await query.message.edit_text("✅ Ви видалили товар", reply_markup=back_mk)

@router.callback_query(AdminHandler.filter(F.value == "users"))
async def setup_users(query: CallbackQuery, callback_data: AdminHandler):
    await query.message.edit_text("Введіть id користувача:", reply_markup=clear_state_mk)
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
    await query.message.edit_text("👑 Адмін панель", reply_markup=admin_mk)
    await query.answer()
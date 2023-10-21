import sqlite3
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

con = sqlite3.connect("database.db")
cur = con.cursor()

class AdminHandler(CallbackData, prefix="admin"):
    value: str
    action: str = "_"

class RemoveItems(CallbackData, prefix="remove_item"):
    type: str
    id: int

admin_btns = [
    [InlineKeyboardButton(text="🏪 Змінити категорії", callback_data=AdminHandler(value = "category").pack())],
    [InlineKeyboardButton(text="🛍️ Змінити товари", callback_data=AdminHandler(value = "lots").pack())],
    [InlineKeyboardButton(text="👤 Змінити інформацію користувача", callback_data=AdminHandler(value = "users").pack())],
]
admin_mk = InlineKeyboardMarkup(inline_keyboard=admin_btns)

setup_cut_btns = [
    [InlineKeyboardButton(text="➕ Додати категорію", callback_data=AdminHandler(value = "category", action="add").pack())],
    [InlineKeyboardButton(text="➖ Видалити категорію", callback_data=AdminHandler(value = "category", action="remove").pack())],
    [InlineKeyboardButton(text="📋 Список категорій", callback_data=AdminHandler(value = "category", action="list").pack())],
    [InlineKeyboardButton(text="🔙 Назад", callback_data=AdminHandler(value = "back").pack())],
]
setup_cut_mk = InlineKeyboardMarkup(inline_keyboard=setup_cut_btns)

setup_lots_btns = [
    [InlineKeyboardButton(text="➕ Додати товар", callback_data=AdminHandler(value = "lots", action="add").pack())],
    [InlineKeyboardButton(text="➖ Видалити товар", callback_data=AdminHandler(value = "lots", action="remove").pack())],
    [InlineKeyboardButton(text="📋 Список товарів", callback_data=AdminHandler(value = "lots", action="list").pack())],
    [InlineKeyboardButton(text="🔙 Назад", callback_data=AdminHandler(value = "back").pack())],
]
setup_lot_mk = InlineKeyboardMarkup(inline_keyboard=setup_lots_btns)

back_mk = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data=AdminHandler(value = "back").pack())],])

clear_state_mk = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Скасувати", callback_data=AdminHandler(value = "clear_state").pack())]]
    )

def remove_category_mk():
    builder = InlineKeyboardBuilder()
    categories_list = cur.execute("SELECT * FROM categories").fetchall()

    for category in categories_list:
        builder.add(InlineKeyboardButton
                    (text=category[1],
                    callback_data=RemoveItems(type="category", id = category[0]).pack()))

    builder.button(text="🔙 Назад", callback_data=AdminHandler(value = "back").pack())
    builder.adjust(1)
    return builder.as_markup()

def categories_list_mk():
    builder = InlineKeyboardBuilder()
    categories_list = cur.execute("SELECT * FROM categories").fetchall()

    for category in categories_list:
        builder.add(InlineKeyboardButton(text=category[1], callback_data=AdminHandler(value = "category_click").pack()))

    builder.button(text="🔙 Назад", callback_data=AdminHandler(value = "back").pack())
    builder.adjust(1)
    return builder.as_markup()
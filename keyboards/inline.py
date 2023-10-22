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

def smart_builder(type: str, action: str, id: int = None):
    builder = InlineKeyboardBuilder()

    db = {
        "category": cur.execute(f"SELECT * FROM categories").fetchall(),
        "lot": cur.execute(f"SELECT * FROM lots").fetchall(),
        "lot_with_cat": cur.execute(f"SELECT * FROM lots WHERE category = ?",(id,)).fetchall(),
    }
    for category in db[type]:
        callback_data = {
            "remove": RemoveItems(type=type, id = category[0]).pack(),
            "list": AdminHandler(value = "category_click").pack(),
            "add_lot_category": AdminHandler(value = "add_lot_category", action=str(category[0])).pack(),
            "select_cat_for_remove_lot": AdminHandler(value = "select_cat_for_remove_lot", action=str(category[0])).pack(),
        }
        
        builder.add(InlineKeyboardButton
                    (text=category[1],
                    callback_data=callback_data[action]))

    builder.button(text="🔙 Назад", callback_data=AdminHandler(value = "back").pack())
    builder.adjust(1)
    return builder.as_markup()
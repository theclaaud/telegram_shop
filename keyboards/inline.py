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

class UserChoose(CallbackData, prefix="user"):
    type: str
    id: int = 0

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

def smart_builder(type: str, action: str, id: int = None, back_type: int = None):
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
            "user_category": UserChoose(type = "category", id=category[0]).pack(),
            "choose_lot": UserChoose(type = "lot", id=category[0]).pack(),
        }
        
        builder.add(InlineKeyboardButton
                    (text=f"{category[1]} {['' if type!='lot_with_cat' else f'| {category[3]} ₴'][0]}",
                    callback_data=callback_data[action]))
        
    match back_type:
        case 1:
            builder.attach(back_builder(to="admin"))
        case 2:
            builder.attach(back_builder(to="categories"))
        case 3:
            builder.attach(back_builder(to="lots"))
        case _:
            pass

    builder.adjust(1)
    return builder.as_markup()

def back_builder(to: str, id: int = None):
    builder = InlineKeyboardBuilder()

    match to:
        case "admin":
            builder.button(text="🔙 Назад", callback_data=AdminHandler(value = "back").pack())
        case "categories":
            builder.button(text="🔙 Назад", callback_data=UserChoose(type = "back_categories").pack())
        case "lots":
            builder.button(text="🔙 Назад", callback_data=UserChoose(type = "category", id=id).pack())

    builder.adjust(1)
    return builder

def buy_builder(id: int,category_id: int, price: int):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"{price}₴ | Купити ✅", callback_data=UserChoose(type = "buy_lot",id = id).pack())
    builder.attach(back_builder(to="lots", id=category_id))

    builder.adjust(1)
    return builder.as_markup()
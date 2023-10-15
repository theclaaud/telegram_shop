from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class AdminHandler(CallbackData, prefix="admin"):
    value: str
    action: str = "_"

admin_btns = [
    [InlineKeyboardButton(text="🏪 Змінити категорії", callback_data=AdminHandler(value = "category").pack())],
    [InlineKeyboardButton(text="🛍️ Змінити товари", callback_data=AdminHandler(value = "lots").pack())],
    [InlineKeyboardButton(text="👤 Змінити інформацію користувача", callback_data=AdminHandler(value = "users").pack())],
]
admin_mk = InlineKeyboardMarkup(inline_keyboard=admin_btns)

setup_cut_btns = [
    [InlineKeyboardButton(text="Додати категорію", callback_data=AdminHandler(value = "category", action="add").pack())],
    [InlineKeyboardButton(text="Видалити категорію", callback_data=AdminHandler(value = "category", action="remove").pack())],
    [InlineKeyboardButton(text="Список категорій", callback_data=AdminHandler(value = "category", action="list").pack())],
    [InlineKeyboardButton(text="Назад", callback_data=AdminHandler(value = "back").pack())],
]
setup_cut_mk = InlineKeyboardMarkup(inline_keyboard=setup_cut_btns)
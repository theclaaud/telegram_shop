from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_btns = [
    [InlineKeyboardButton(text="🏪 Змінити категорії", callback_data="adm:cut")],
    [InlineKeyboardButton(text="🛍️ Змінити товари", callback_data="adm:prd")],
    [InlineKeyboardButton(text="👤 Змінити інформацію користувача", callback_data="adm:usr")],
]
admin_mk = InlineKeyboardMarkup(inline_keyboard=admin_btns)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main_bnts = [
    [KeyboardButton(text="🛒 Каталог товарів"),KeyboardButton(text="🔎 Пошук")],
    [KeyboardButton(text="🤵 Особистий кабінет"),KeyboardButton(text="⁉️ Допомога")]
]
main_mk = ReplyKeyboardMarkup(keyboard=main_bnts,resize_keyboard=True)

admin_btns = [
    [InlineKeyboardButton(text="🏪 Змінити категорії", callback_data="adm:cut")],
    [InlineKeyboardButton(text="🛍️ Змінити товари", callback_data="adm:prd")],
    [InlineKeyboardButton(text="👤 Змінити інформацію користувача", callback_data="adm:usr")],
]
admin_mk = InlineKeyboardMarkup(inline_keyboard=admin_btns)


# main_mk = ReplyKeyboardBuilder()
# main_mk.button(text="test")
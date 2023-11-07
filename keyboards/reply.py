from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_bnts = [
    [KeyboardButton(text="🛒 Каталог товарів")],
    [KeyboardButton(text="🤵 Особистий кабінет"),KeyboardButton(text="⁉️ Допомога")]
]
main_mk = ReplyKeyboardMarkup(keyboard=main_bnts,resize_keyboard=True)

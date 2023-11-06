import sqlite3
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from keyboards.inline import UserChoose, smart_builder, buy_builder

router = Router()
con = sqlite3.connect("database.db")
cur = con.cursor()

@router.callback_query(UserChoose.filter(F.type == "back_categories"))
async def category_list(query: CallbackQuery, callback_data: UserChoose):
    await query.message.edit_text("Виберіть потрібну <b>категорію:</b>", reply_markup=smart_builder(type="category", action="user_category"))

@router.callback_query(UserChoose.filter(F.type == "category"))
async def choose_lot(query: CallbackQuery, callback_data: UserChoose):
    await query.message.delete()
    await query.message.answer("Добре, тепер виберіть товар", reply_markup=smart_builder(type="lot_with_cat", action="choose_lot", id=callback_data.id, back_type=2))

@router.callback_query(UserChoose.filter(F.type == "lot"))
async def lot(query: CallbackQuery, callback_data: UserChoose):
    lot_data = cur.execute("SELECT * FROM lots WHERE id = ?",(callback_data.id,)).fetchone()
    category_title = cur.execute("SELECT title FROM categories WHERE id = ?",(lot_data[5],)).fetchone()[0]
    
    await query.message.delete()
    await query.message.answer_photo(photo=lot_data[4],caption=f"<b>{lot_data[1]}</b> \n{lot_data[3]}₴ \n{category_title}", reply_markup=buy_builder(lot_data[0],lot_data[5], lot_data[3]))
    # await query.message.edit_text(f"<b>{lot_data[1]}</b> \n{lot_data[3]}₴ \n{category_title}", reply_markup=buy_builder(lot_data[0],lot_data[5], lot_data[3]))
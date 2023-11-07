import sqlite3
import os
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery, SuccessfulPayment
from keyboards.inline import UserChoose, smart_builder, buy_builder
from dotenv import load_dotenv

router = Router()
con = sqlite3.connect("database.db")
cur = con.cursor()
load_dotenv(".env")

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
    await query.message.answer_photo(photo=lot_data[4],caption=f"<b>{lot_data[1]} - {category_title}</b>\n{lot_data[2]}", reply_markup=buy_builder(lot_data[0],lot_data[5], lot_data[3]))
    # await query.message.edit_text(f"<b>{lot_data[1]}</b> \n{lot_data[3]}₴ \n{category_title}", reply_markup=buy_builder(lot_data[0],lot_data[5], lot_data[3]))

@router.callback_query(UserChoose.filter(F.type == "buy_lot"))
async def send_invoice(query: CallbackQuery, callback_data: UserChoose):
    lot_data = cur.execute("SELECT * FROM lots WHERE id = ?",(callback_data.id,)).fetchone()
    
    await query.message.answer_invoice(title=lot_data[1],
                                       description=lot_data[2],
                                       payload=str(lot_data[0]),
                                       provider_token=os.getenv("PAY_ID"),
                                       currency="uah",
                                       prices=[LabeledPrice(label=lot_data[1], amount=lot_data[3]*100)],
                                    #    photo_url=lot_data[4],
                                       need_name=True,
                                       need_phone_number=True,
                                       need_email=True,
                                       need_shipping_address=True,
                                       )
    await query.answer()

@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot):
    lot = cur.execute("SELECT * FROM lots WHERE id = ?",(message.successful_payment.invoice_payload,)).fetchone()
    cur.execute("INSERT INTO orders (buyer_id, lot_id, summ) VALUES (?, ?, ?)", (message.from_user.id, lot[0], str(message.successful_payment.total_amount)[:-2]))
    con.commit()
    await bot.send_message(
        chat_id=os.getenv("ORDERS_CHAT_ID"),
        text=f"Замовник: @{message.from_user.username}\nСума: {str(message.successful_payment.total_amount)[:-2]}₴\nТовар: {lot[1]} \n"+"\n".join([f"{key}: {value}" for key, value in message.successful_payment.order_info]),
        )
    await message.answer("Ваше замовлення створено, з вами зв'яжеться адміністратор.")
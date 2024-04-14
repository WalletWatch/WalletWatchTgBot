from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from db.db import Database

db = Database()

def make_wallet_keyboard(user_id):
    wallets = db.get_user_wallets(user_id)
    inline_keyboard = InlineKeyboardBuilder()

    for i in wallets:
        inline_keyboard.add(types.InlineKeyboardButton(text=i[1], callback_data=str(i[0])))
    inline_keyboard.adjust(3)

    return inline_keyboard.as_markup()

def make_token_keyboard(wallet_id):
    wallets = db.get_wallet_balances(wallet_id=wallet_id)
    inline_keyboard = InlineKeyboardBuilder()

    for i in wallets:
        name = i[1]
        inline_keyboard.add(types.InlineKeyboardButton(text=f"{name}", callback_data="token_"+str(i[0])))
    inline_keyboard.adjust(4)

    return inline_keyboard.as_markup()

def make_kb_main():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='📬 Баланс кошельков', callback_data='wallets'))
    builder.add(types.InlineKeyboardButton(text='📜 Посмотреть токены', callback_data='walletmenu'))
    builder.add(types.InlineKeyboardButton(text='❌ Удалить кошелёк', callback_data='deletewallet'))
    builder.add(types.InlineKeyboardButton(text='📥 Добавить кошелёк', callback_data='addwallet'))
    builder.add(types.InlineKeyboardButton(text='🔔 Помощь', callback_data='help'))

    builder.adjust(2, 1, 1)

    return builder.as_markup(resize_keyboard=True)

def make_token_menu(token_id, track):
    builder = InlineKeyboardBuilder()
    
    text_track = "Не уведомлять об изменении" if track else "Уведомлять об изменении" 
    builder.add(types.InlineKeyboardButton(text=text_track, callback_data="track_"+str(token_id)))
    builder.add(types.InlineKeyboardButton(text="Поменять значение", callback_data="delta_"+str(token_id)))

    return builder.as_markup(resize_keyboard=True)


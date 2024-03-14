from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from utils import wallet_list, network_list, balance_list

def make_wallet_keyboard():
    wallets = wallet_list()
    inline_keyboard = InlineKeyboardBuilder()

    for i in wallets:
        inline_keyboard.add(types.InlineKeyboardButton(text=i['wallet_name'], callback_data=str(i['id'])))
    inline_keyboard.adjust(3)

    return inline_keyboard.as_markup()

def make_token_keyboard():
    wallets = balance_list()
    inline_keyboard = InlineKeyboardBuilder()

    for i in wallets:
        name = i['wallet_name']
        token = i['asset']
        inline_keyboard.add(types.InlineKeyboardButton(text=f"{name}-{token}", callback_data=str(i['id'])))
    inline_keyboard.adjust(2)

    return inline_keyboard.as_markup()

def make_network_keyboard():
    networks = network_list()
    inline_keyboard = InlineKeyboardBuilder()

    for i in networks:
        inline_keyboard.add(types.InlineKeyboardButton(text=i['network'], callback_data=str(i['id'])))
    inline_keyboard.adjust(3)

    return inline_keyboard.as_markup()

def make_kb_main():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='📜 Кошельки', callback_data='walletmenu'))
    builder.add(types.InlineKeyboardButton(text='💰 Токены', callback_data='tokenmenu'))
    builder.add(types.InlineKeyboardButton(text='📬 Подписаться на обновления', callback_data='connect'))
    builder.add(types.InlineKeyboardButton(text='🚫 Отписаться от обновлений', callback_data='stop'))
    builder.add(types.InlineKeyboardButton(text='🔔 Меню', callback_data='menu'))

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def make_kb_wallets():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='💰 Посмотреть кошельки', callback_data='wallets'))
    builder.add(types.InlineKeyboardButton(text='➕ Добавить кошелёк', callback_data='addwallet'))
    builder.add(types.InlineKeyboardButton(text='❌ Удалить кошелёк', callback_data='deletewallet'))

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def make_kb_tokens():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='💰 Посмотреть балансы', callback_data='tokens'))
    builder.add(types.InlineKeyboardButton(text='➕ Добавить токен', callback_data='addtoken'))
    builder.add(types.InlineKeyboardButton(text='❌ Удалить токен', callback_data='deletetoken'))

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

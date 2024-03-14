from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from datetime import datetime
import websockets
import json

router_websocket = Router()

connected_users = set()

@router_websocket.message(Command("connect"))
async def connect_to_websocket(message: Message):
    connected_users.add(message.from_user.id)
    await message.answer("🚀 Теперь вы будете получать обновления.")

@router_websocket.callback_query(F.data =="connect")
async def connect_to_websocket(callback: CallbackQuery):
    connected_users.add(callback.from_user.id)
    await callback.message.answer("🚀 Теперь вы будете получать обновления.")


@router_websocket.message(Command("stop"))
async def disconnect_from_websocket(message: Message):
    connected_users.discard(message.from_user.id)
    await message.answer("🔌 Вы отключились от обновлений.")

@router_websocket.callback_query(F.data =="stop")
async def disconnect_from_websocket(callback: CallbackQuery):
    connected_users.discard(callback.from_user.id)
    await callback.message.answer("🔌 Вы отключились от обновлений.")



# Функция для отправки сообщения пользователю
async def send_message_to_user(bot, message, user_id):
    data = json.loads(message)

    name = data['balance']['asset']
    wallet = data['balance']['wallet_name']
    network = data['balance']['network_name']
    balance = data['balance']['balance']
    price = data['balance']['price']
    value = balance * price

    start_time = datetime.strptime(data['balance']['updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
    current_time = datetime.now()
    time_difference = current_time - start_time

    await bot.send_message(chat_id=user_id, text=f"*Кошелёк*: *{wallet}*\n\
*Токен*: *{name}*\n\
    - Количество: *{round(balance, 2)} {name}*\n\
    - Цена: *${round(price, 4)}* за 1 {name}\n\
    - Сумма: *${round(value, 2)}*\n\
    - Сеть: *{network}*\n\
    - Обновлено: *{time_difference}*\n",
        parse_mode='Markdown'
    )


host = "3f9215732d0c.vps.myjino.ru"
# host = "127.0.0.1:8000"

# WebSocket клиент
async def websocket_client(bot):
    async with websockets.connect(f'ws://{host}/ws/wallet/') as websocket:
        try:
            while True:
                message = await websocket.recv()
                for user_id in connected_users:
                    await send_message_to_user(bot, message, user_id)
        except websockets.ConnectionClosed:
            for user_id in connected_users:
                await bot.send_message(chat_id=user_id, 
                    text=f"🔥 Кажется, возникла небольшая неполадка. Но не беспокойтесь, наша команда уже принимает меры для исправления ситуации!",
                    parse_mode='Markdown'
                )
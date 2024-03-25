import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = "7020669369:AAEZZVBUfTN6h6CkeTjsDUPg3lK4BPzXVlI"

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.wallet_handlers import router_wallet
from handlers.balance_handler import router_balance
from handlers.main_handler import router_main
from handlers.websocket_handler import router_websocket, websocket_client


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router_wallet)
    dp.include_router(router_balance)
    dp.include_router(router_main)
    dp.include_router(router_websocket)

    # Запуск WebSocket клиента
    loop = asyncio.get_event_loop()
    loop.create_task(websocket_client(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
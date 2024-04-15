import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.wallet_handlers import router_wallet
from handlers.main_handler import router_main
from db.tasks import update_balances, update_wallets

load_dotenv()
# TOKEN = os.getenv('BOT_TOKEN')
TOKEN = "7020669369:AAEZZVBUfTN6h6CkeTjsDUPg3lK4BPzXVlI"

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router_wallet)
    dp.include_router(router_main)

    # loop = asyncio.get_event_loop()
    # loop.create_task(update_balances(bot))
    # loop.create_task(update_wallets(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
import logging
import asyncio
from aiogram import Bot
from config import *
from aiogram import Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, loop=loop, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def throttling_message(user):
    try:
        await dp.throttle(str(user), rate=1)
    except Throttled:
        await bot.send_message(user, "Too fast. Try again in 1 sec")
        return True


async def on_startup(dp):
    return await bot.set_webhook(url=WEBHOOK_URL)


if __name__ == '__main__':
    from handlers.setup_gauth import *
    from handlers.bot_info import *
    from handlers.buttons import *
    from handlers.decoding import *
    from handlers.encoding import *
    from handlers.main import *
    if Reviews_state:
        from handlers.reviews import *

    if Webhook_state:
        executor.start_webhook(dispatcher=dp, webhook_path="",
                               host=WEBAPP_HOST, port=WEBAPP_PORT, on_startup=on_startup)
    else:
        executor.start_polling(dp)

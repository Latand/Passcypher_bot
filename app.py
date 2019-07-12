import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from config import (I18N_DOMAIN, WEBHOOK_URL, LOCALES_DIR, Reviews_state,
                    TOKEN, Webhook_state, WEBAPP_HOST, WEBAPP_PORT)
from bot.middlewares.language_middleware import setup_middleware

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, loop=loop, parse_mode="HTML")
# storage = MemoryStorage()
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)


async def throttling_message(user):
    try:
        await dp.throttle(str(user), rate=1)
    except Throttled:
        await bot.send_message(user, "Too fast. Try again in 1 sec")
        return True


async def on_startup(dp):
    return await bot.set_webhook(url=WEBHOOK_URL)


# Setup i18n middleware

i18n = setup_middleware(dp)

# Alias for gettext method
_ = i18n.gettext

if __name__ == '__main__':

    if Reviews_state:
        from bot.handlers.reviews import *
    from bot.handlers.setup_gauth import *
    from bot.handlers.bot_info import *
    from bot.handlers.buttons import *
    from bot.handlers.decoding import *
    from bot.handlers.encoding import *
    from bot.handlers.admin_panel import *
    from bot.handlers.main_handlers import *
    from bot.handlers.errors import *

    if Webhook_state:
        executor.start_webhook(dispatcher=dp, webhook_path="",
                               host=WEBAPP_HOST, port=WEBAPP_PORT, on_startup=on_startup)
    else:
        executor.start_polling(dp)

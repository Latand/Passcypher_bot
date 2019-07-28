import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from bot.middlewares.language_middleware import setup_middleware
from config import TOKEN

# from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)
loop = asyncio.get_event_loop()
# Set up storage (either in Redis or Memory)
# storage = MemoryStorage()
storage = RedisStorage2()

bot = Bot(token=TOKEN, loop=loop, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

# Setup i18n middleware
i18n = setup_middleware(dp)

# Alias for gettext method
_ = i18n.gettext

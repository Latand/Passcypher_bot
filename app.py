from aiogram import executor

from config import (WEBHOOK_URL, Reviews_state,
                    Webhook_state, WEBAPP_HOST, WEBAPP_PORT)
from load_all import bot


async def on_startup(dp):
    return await bot.set_webhook(url=WEBHOOK_URL)


if __name__ == '__main__':
    if Reviews_state:
        from bot.handlers.reviews import dp
    from bot.handlers.setup_gauth import dp
    from bot.handlers.bot_info import dp
    from bot.handlers.buttons import dp
    from bot.handlers.decoding import dp
    from bot.handlers.encoding import dp
    from bot.handlers.admin_panel import dp
    from bot.handlers.main_handlers import dp
    from bot.handlers.errors import dp

    if Webhook_state:
        executor.start_webhook(dispatcher=dp, webhook_path="",
                               host=WEBAPP_HOST, port=WEBAPP_PORT, on_startup=on_startup)
    else:
        executor.start_polling(dp)

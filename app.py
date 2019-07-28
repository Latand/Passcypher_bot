import logging
from asyncio import sleep

from aiogram import executor

from config import (WEBHOOK_URL, Reviews_state,
                    Webhook_state, WEBAPP_HOST, WEBAPP_PORT)
from load_all import bot


async def on_startup(dp):
    await on_startup_polling(dp)
    return await bot.set_webhook(url=WEBHOOK_URL)


async def on_startup_polling(dp):
    from bot.utils.sql import sql
    logging.info(f"Wait 20 until MYSQL Starts... initialising MYSQL DATABASE")
    await sleep(20)
    with open("mysql_data/init.sql", "r") as file:
        command = file.read()
    if command:
        logging.info("Loaded SQL command")
    sql.execute(command)
    logging.info("Table created")


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
        executor.start_polling(dp, on_startup=on_startup_polling)

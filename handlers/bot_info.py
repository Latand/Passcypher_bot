import logging

from filters import *
from main_bot import dp
from messages import links
from some_functions import *


@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    await message.reply(links(lang).INSTRUCTION)

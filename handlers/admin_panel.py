from asyncio import sleep

from filters import *
from main_bot import bot, dp
from some_functions import *


@dp.message_handler(IsAdmin(), commands=["send_to_all"])
async def encode_m(message: types.Message):
    increase_message_counter()

    text = message.text.split("/send_to_all")[1]
    result = await sender(text)
    chat_id = message.chat.id
    await message.reply(chat_id, "Готово. Ошибки: {}".format(result))


async def sender(message: str):
    users_list = sql.select(what="chat_id", where="users")
    errors = set()
    for (user,) in users_list:
        try:
            await bot.send_message(chat_id=user, message=message)
        except Exception as err:
            errors.add(err)
        finally:
            await sleep(1)
    return errors

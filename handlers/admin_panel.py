from asyncio import sleep, ensure_future
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated
from google_auth import has_g_auth
from filters import *
from main_bot import bot, dp
from some_functions import *
import logging


@dp.message_handler(IsAdmin(), commands=["send_to_all"])
async def encode_m(message: types.Message):
    increase_message_counter()

    text = message.text.split("/send_to_all")[1]
    result = ensure_future(sender(text))
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Готово. Ошибки: {}".format(result))


async def sender(message: str):
    users_list = sql.select(what="chat_id", where="users")
    errors = set()
    for (user,) in users_list:
        try:
            await bot.send_message(chat_id=user, text=message)
        except (BotBlocked, ChatNotFound, UserDeactivated):
            if not has_g_auth(user):
                try:
                    sql.delete(table="users", where=["chat_id"], what=user)
                except Exception as error:
                    logging.error(error)
        except Exception as err:
            logging.error(err)
            errors.add(err)
        finally:
            await sleep(1)
    return errors

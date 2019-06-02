from asyncio import sleep, ensure_future
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated
from filters import *
from main_bot import bot, dp
from some_functions import *
import logging
import re


@dp.message_handler(IsAdmin(), commands=["send_to_all_ru",
                                         "send_to_all_en",
                                         "send_to_all_ua"])
async def encode_m(message: types.Message):
    increase_message_counter()

    result = ensure_future(sender(message))
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"Готово. Ошибки: {result}")


async def sender(message: types.Message):
    command = re.match(r"(/send_to_all_(\w\w))", message.text)
    lang = command.group(2)
    text = message.text.split(command.group(1))[1]
    if not text:
        return 0

    users_list = sql.select(what="chat_id", where="users", condition={"language": lang})
    total_users = len(users_list)
    to_edit = await bot.send_message(admin_id, f"Всего {total_users}. Послано 0 Юзерам. Текст:{text}")
    errors = set()
    count = 0
    for (user,) in users_list:
        try:
            await bot.send_message(chat_id=user, text=text)

        except (BotBlocked, ChatNotFound, UserDeactivated):
            sql.update(table="users", condition={"chat_id": user}, blocked=1)
            logging.info(f"User {user} blocked bot")
        except Exception as err:
            logging.error(err)
            errors.add(err)
        finally:
            await sleep(0.4)
            count += 1
            if count % 10 == 0:
                await to_edit.edit_text(f"Всего {total_users}. Послано {count} Юзерам.")
    return len(errors)

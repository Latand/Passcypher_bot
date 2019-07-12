import logging
import re
from asyncio import sleep

from aiogram import types
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated

from app import bot, dp
from bot.aiogram_help.filters import IsAdmin, admin_id
from bot.utils.some_functions import increase_message_counter, sql


@dp.message_handler(IsAdmin(), commands=["send_to_all_ru",
                                         "send_to_all_en",
                                         "send_to_all_uk"])
async def encode_m(message: types.Message):
    increase_message_counter()

    result = await sender(message)
    await message.reply(f"Заблокировано {result}")


@dp.message_handler(IsAdmin(), commands=["check_blocked"])
async def encode_m(message: types.Message):
    increase_message_counter()
    await checker()


async def sender(message: types.Message):
    command = re.match(r"(/send_to_all_(\w\w))", message.text)
    lang = command.group(2)
    text = message.text.split(command.group(1))[1]
    if not text:
        return 0

    users_list = sql.select(what="chat_id", where="users", condition={"language": lang,
                                                                      "blocked": 0})
    total_users = len(users_list)
    to_edit = await bot.send_message(admin_id, f"Всего живых {total_users}. Послано 0 Юзерам. Текст:{text}")
    errors = 0
    count = 0
    for (user,) in users_list:
        try:
            await bot.send_message(chat_id=user, text=text)

        except (BotBlocked, ChatNotFound, UserDeactivated):
            sql.update(table="users", condition={"chat_id": user}, blocked=1)
            logging.info(f"User {user} blocked bot")
            errors += 1

        except Exception as err:
            logging.error(err)
        finally:
            await sleep(0.04)
            count += 1
            if count % 10 == 0:
                await to_edit.edit_text(f"Всего {total_users}. Послано {count} Юзерам.")
    return errors


async def checker():

    users_list = sql.select(what="chat_id", where="users", condition={"blocked": 0})
    total_users = len(users_list)
    to_edit = await bot.send_message(admin_id, f"Всего {total_users} юзеров.")
    count = 0
    for (user,) in users_list:
        try:
            await bot.send_chat_action(chat_id=user, action=types.chat.ChatActions.TYPING)

        except (BotBlocked, ChatNotFound, UserDeactivated):

            sql.update(table="users", condition={"chat_id": user}, blocked=1)
            logging.info(f"User {user} blocked bot")
            count += 1
        finally:
            await sleep(0.4)

    await to_edit.edit_text(f"Всего живых {total_users}. Заблокировано {count} Юзеров.")

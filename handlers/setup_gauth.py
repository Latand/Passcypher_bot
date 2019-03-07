# from messages import texts as imported_text
# from languages import *
from some_functions import *
from inline_button import *
from google_auth import *
import binascii
from main_bot import bot, dp, logging
from states import *
from filters import *
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=["g_auth_info"])
async def info(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = get_text(lang, "g_auth info")
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[get_text(lang, "enable_g_auth")],
        callback=["g_auth_setup"]))


@dp.message_handler(commands=["reset_google_auth"])
async def info(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    if has_g_auth(chat_id):
        if enabled_g_auth(chat_id):
            await bot.send_message(chat_id, get_text(lang, "reset gauth"),
                                   reply_markup=inlinemarkups(
                                       text=[get_text(lang, "turn off")],
                                       callback=["turn 0"]))
        else:

            await bot.send_message(chat_id, get_text(lang, "reset gauth"),
                                   reply_markup=inlinemarkups(
                                       text=[get_text(lang, "turn on")],
                                       callback=["turn 1"]))
    else:
        await bot.send_message(chat_id, get_text(lang, "not set"))


@dp.callback_query_handler(Callbacks("turn", contains=True))
async def g_auth(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    enabled = call.data.split()[1]
    sql.update(table="users", enabled=enabled, condition={"chat_id": chat_id})
    try:
        await bot.edit_message_text(text=get_text(lang, "done"),
                                    chat_id=chat_id,
                                    message_id=call.message.message_id)
    except Exception as e:
        logging.error(f"{e}")


@dp.callback_query_handler(Callbacks("g_auth_setup"))
async def g_auth(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    try:
        await bot.edit_message_reply_markup(chat_id, message_id=call.message.message_id)
    except Exception as e:
        logging.error(f"{e}")

    if has_g_auth(chat_id):
        await bot.send_message(chat_id, get_text(lang, "already enabled"))
        return

    await bot.send_message(chat_id, get_text(lang, "google_auth setup 1"), reply_markup=inlinemarkups(
        text=[get_text(lang, "continue")],
        callback=["continue"]))
    await GoogleAuth.ONE.set()


@dp.callback_query_handler(state=GoogleAuth.ONE)
async def g_auth(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    try:
        await bot.edit_message_reply_markup(chat_id, message_id=call.message.message_id)
    except Exception as e:
        logging.error(f"{e}")
    if has_g_auth(chat_id):
        await bot.send_message(chat_id, get_text(lang, "already enabled"))
        return

    code, link, qr_code = create_google_auth(chat_id)
    await bot.send_message(chat_id, get_text(lang, "google_auth setup 2"))
    message_1 = (await bot.send_message(chat_id, code)).message_id

    message_2 = (await bot.send_photo(chat_id, qr_code,
                                      f"{link}")).message_id
    await bot.send_message(chat_id, get_text(lang, "google_auth setup 3"))

    await state.update_data(message_1=message_1, message_2=message_2)
    await GoogleAuth.next()


@dp.message_handler(state=GoogleAuth.TWO)
async def g_auth(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    try:
        ver = verify(chat_id, message.text)
    except binascii.Error:
        await bot.send_message(chat_id, get_text(lang, "invalid code"))
        return
    if ver:
        async with state.proxy() as data:
            message_1 = data.get("message_1")
            message_2 = data.get("message_2")
        await bot.delete_message(chat_id, message_1)
        await bot.delete_message(chat_id, message_2)
        await bot.send_message(chat_id, get_text(lang, "confirm yes"))
        await state.finish()
    else:
        await bot.send_message(chat_id, get_text(lang, "confirm no"))

import logging

from filters import *
from inline_button import ListOfButtons
from main_bot import bot, dp
from messages import allowed_chars
from some_functions import *


@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = get_text(lang, "describe en 1")
    await bot.send_message(chat_id, text, reply_markup=ListOfButtons(
        text=[get_text(lang, "next")],
        callback=["describe_en 2"]
    ).inline_keyboard)
    text = get_text(lang, "describe de 1")
    await bot.send_message(chat_id, text, reply_markup=ListOfButtons(
        text=[get_text(lang, "next")],
        callback=["describe_de 2"]
    ).inline_keyboard)


@dp.callback_query_handler(Callbacks("describe_en", contains=True))
async def next_page(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    try:
        page = int(call.data.split()[1])
    except IndexError as err:
        logging.error(f"Error {err}. Call: {call.data}")
        return
    buts, calls = [], []
    if page > 1:
        buts.append(get_text(lang, "prev"))
        calls.append(f"describe_en {page - 1}")
    if page < 4:
        buts.append(get_text(lang, "next"))
        calls.append(f"describe_en {page + 1}")
    await bot.edit_message_text(chat_id=chat_id, text=get_text(lang, f"describe en {page}").format(
        allowed_chars=allowed_chars),
                                message_id=call.message.message_id,
                                reply_markup=ListOfButtons(
                                    text=buts,
                                    callback=calls,
                                    align=[len(buts)]
                                ).inline_keyboard)


@dp.callback_query_handler(Callbacks("describe_de", contains=True))
async def next_page(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    page = int(call.data.split()[1])
    buts, calls = [], []
    if page > 1:
        buts.append(get_text(lang, "prev"))
        calls.append(f"describe_de {page - 1}")
    if page < 3:
        buts.append(get_text(lang, "next"))
        calls.append(f"describe_de {page + 1}")
    await bot.edit_message_text(chat_id=chat_id, text=get_text(lang, f"describe de {page}"),
                                message_id=call.message.message_id,
                                reply_markup=ListOfButtons(
                                    text=buts,
                                    callback=calls,
                                    align=[len(buts)]
                                ).inline_keyboard)

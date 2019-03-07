from some_functions import *
from inline_button import *
from google_auth import *
from main_bot import bot, dp, logging
from states import *
from filters import *
from messages import allowed_chars, Other_Texts
from aiogram.dispatcher import FSMContext


@dp.message_handler(Buttons("ENCODE"))
async def encode_m(message: types.Message, state: FSMContext):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, get_text(lang, "encode master"))
        await Encode.MASTER_PASSWORD.set()
    else:
        await state.update_data(master_pass=get_google_auth(chat_id))
        await Encode.PASSWORD.set()
        await bot.send_message(chat_id, get_text(lang, "password").format(allowed_chars=allowed_chars))


@dp.message_handler(Buttons("DECODE"))
async def decode_m(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = get_text(lang, "describe de 1")
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[get_text(lang, "next")],
        callback=["describe_de 2"]
    ))


@dp.message_handler(Buttons("INFO"))
async def info_m(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = get_text(lang, "describe en 1")
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[get_text(lang, "next")],
        callback=["describe_en 2"]
    ))
    text = get_text(lang, "describe de 1")
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[get_text(lang, "next")],
        callback=["describe_de 2"]
    ))


@dp.message_handler(Buttons("LANGUAGE"))
async def language_set(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    await bot.send_message(chat_id,
                           Other_Texts.SET_LANGUAGE_MESSAGE.format(message.from_user.first_name),
                           reply_markup=inlinemarkups(
                               text=["English", "Русский"],
                               callback=["language en", "language ru"]
                           ))


@dp.message_handler(Buttons("GOOGLE_AUTH"))
async def set_google_auth(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    if has_g_auth(chat_id):
        if enabled_g_auth(chat_id):
            await bot.send_message(chat_id, get_text(lang, "reset gauth"), reply_markup=inlinemarkups(
                text=[get_text(lang, "turn off")],
                callback=["turn 0"]))
        else:

            await bot.send_message(chat_id, get_text(lang, "reset gauth"), reply_markup=inlinemarkups(
                text=[get_text(lang, "turn on")],
                callback=["turn 1"]))
    else:
        await bot.send_message(chat_id, get_text(lang, "not set"))

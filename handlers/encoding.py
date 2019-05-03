from aiogram.dispatcher import FSMContext
import asyncio
from encode import encode
from filters import *
from google_auth import *
from inline_button import *
from main_bot import bot, dp
from messages import allowed_chars
from some_functions import *
from states import *


@dp.message_handler(commands=["encode", "e"])
async def encode_start(message: types.Message, state: FSMContext):
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


@dp.message_handler(state=Encode.MASTER_PASSWORD)
async def encoded(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    if "/g_auth_info" == message.text:
        text = get_text(lang, "g_auth info")
        await bot.send_message(chat_id, text, reply_markup=ListOfButtons(
            text=[get_text(lang, "enable_g_auth")],
            callback=["g_auth_setup"]).inline_keyboard)
        await state.finish()
        return
    await state.update_data(master_pass=message.text)
    await Encode.PASSWORD.set()
    await bot.send_message(chat_id, get_text(lang, "password").format(allowed_chars=allowed_chars))

    await asyncio.sleep(10)
    await message.delete()


@dp.message_handler(state=Encode.PASSWORD, content_types=types.ContentType.TEXT)
async def encoded(message: types.Message, state: FSMContext):
    increase_message_counter(password=True)
    chat_id = message.chat.id
    lang = get_language(chat_id)
    master_pass = (await state.get_data()).get("master_pass")
    if len(message.text) > 400:
        await bot.send_message(chat_id, get_text(lang, "large"))
        return
    elif not master_pass:
        await message.reply("Master Password not found.")
        await state.finish()
        await asyncio.sleep(10)
        await message.delete()
    text, code = encode(message.text.replace("\n", "\\n"), master_pass)
    if master_pass == get_google_auth(chat_id):
        hint = "Google Authenticator"
    else:
        hint = master_pass[:2] + "***********"
    await bot.send_message(chat_id, get_text(lang, "result_encode").format(
        passw=text, code=code,
        hint=f"{hint}"
    ))
    await state.finish()
    await asyncio.sleep(10)
    await message.delete()


@dp.message_handler(state=Encode.PASSWORD, content_types=types.ContentType.DOCUMENT)
async def encoded(message: types.Message, state: FSMContext):
    increase_message_counter(password=True)
    chat_id = message.chat.id
    lang = get_language(chat_id)
    master_pass = (await state.get_data()).get("master_pass")
    file_id = message.document.file_id
    await bot.download_file_by_id(file_id, "to_encode.txt")
    with open("to_encode.txt", "r") as file:
        try:
            text = file.read().replace("\n", "\\n")
        except UnicodeDecodeError:
            await bot.send_message(chat_id, "INVALID FILE")
            await state.finish()
            return

    text, code = encode(text, master_pass)
    with open("encoded.txt", "a") as file:
        file.write(get_text(lang, "result_encode_doc").format(
            passw=text, code=code,
            hint=f"{master_pass[:2]}***********"))
    await bot.send_document(chat_id, open("encoded.txt", "rb"))

    with open("encoded.txt", "w") as file:
        file.write(" ")

    with open("to_encode.txt", "w") as file:
        file.write(" ")
    await state.finish()

    await asyncio.sleep(10)
    await message.delete()

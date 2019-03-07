from some_functions import *
from inline_button import *
from google_auth import *
from main_bot import bot, dp, logging
from states import *
from filters import *
from aiogram.dispatcher import FSMContext
from messages import Other_Texts
from decode import decode
import re
import binascii


@dp.message_handler(regexp="#encoded_pass")
async def decode_start(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    enc = message.text.replace("\n", " ")
    try:
        encoded = re.findall("#encoded_pass: '(.*)'.*#", enc)[0]
        code = re.findall("#key: '(.*)'", enc)[0]
    except IndexError:
        await bot.send_message(chat_id, "Error")
        return
    await state.update_data(password=encoded, code=code)
    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, get_text(lang, "encode master"))
    else:
        await bot.send_message(chat_id, get_text(lang, "g_auth decode"))
    await Decode.MASTER_PASSWORD.set()


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def decode_start(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    file_id = message.document.file_id
    await bot.download_file_by_id(file_id, "to_decode.txt")
    with open("to_decode.txt", "r") as file:
        try:
            text = file.read()
        except UnicodeDecodeError:
            await bot.send_message(chat_id, "INVALID FILE")
            return
    expression = re.compile(f"{Other_Texts.START}(.*){Other_Texts.END}")
    try:
        extract_encoded = expression.findall(text)[0]

    except IndexError:
        await bot.send_message(chat_id, "Error. Wrong file")
        return
    expression = re.compile(f"{Other_Texts.END}(.*){Other_Texts.END_CODE}")
    code = expression.findall(text)[0]
    await state.update_data(password=extract_encoded, code=code, doc=True)

    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, get_text(lang, "encode master"))
    else:
        await bot.send_message(chat_id, get_text(lang, "g_auth decode"))
    await Decode.MASTER_PASSWORD.set()


@dp.message_handler(state=Decode.MASTER_PASSWORD)
async def decode_1(message: types.Message, state: FSMContext):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    en_password = (await state.get_data()).get("password")
    code = (await dp.current_state().get_data())["code"]
    if not enabled_g_auth(chat_id):
        master = message.text
    else:
        if message.text == "/cancel":
            await bot.send_message(chat_id, "OK.")
            await dp.current_state().reset_state()
            return
        try:
            if verify(chat_id, message.text):
                master = get_google_auth(chat_id)
            else:
                await bot.send_message(chat_id, get_text(lang, "invalid code"))
                return
        except binascii.Error:
            await bot.send_message(chat_id, get_text(lang, "invalid code"))
            return

    password = (decode(master, en_password, code)).replace("\\n", "\n")

    if (await state.get_data()).get("doc"):

        with open("decoded.txt", "w") as file:
            file.write(password.replace("\\n", "\n"))
        await bot.send_document(chat_id, open("decoded.txt", "rb"))
        with open("decoded.txt", "w") as file:
            file.write(" ")
    else:
        await bot.send_message(chat_id, get_text(lang, "decoded_result").format(
            password=password
        ))
    await state.finish()


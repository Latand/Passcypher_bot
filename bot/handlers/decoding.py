import asyncio
import binascii
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest

from app import bot, dp, _
from bot.aiogram_help.states import Decode
from bot.utils.decode import decode
from bot.utils.google_auth import enabled_g_auth, get_google_auth, has_g_auth, verify
from bot.utils.some_functions import increase_message_counter
from bot.utils.some_functions import Other_Texts


@dp.message_handler(regexp="ENCRYPTION STARTS HERE")
async def decode_start(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    text = message.text
    expression = re.compile(f"{Other_Texts.START}(.*){Other_Texts.END}")
    try:
        extract_encoded = expression.findall(text)[0]

    except IndexError:
        await bot.send_message(chat_id, _("Error. Wrong file"))
        return
    expression = re.compile(f"{Other_Texts.END}(.*){Other_Texts.END_CODE}")
    code = expression.findall(text)[0]

    await state.update_data(password=extract_encoded, code=code)
    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, _("""
Please enter your master password.
You can make everything faster with Google Authenticator! 
Press /g_auth_info

"""))
    else:
        await bot.send_message(chat_id, _("Enter the code from the app"))
    await Decode.MASTER_PASSWORD.set()


@dp.message_handler(regexp="#encoded_pass")
async def decode_start(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    enc = message.text.replace("\n", " ")
    try:
        encoded = re.findall("#encoded_pass: '(.*)'.*#", enc)[0]
        code = re.findall("#key: '(.*)'", enc)[0]
    except IndexError:
        await bot.send_message(chat_id, _("Error"))
        return
    await state.update_data(password=encoded, code=code)
    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, _("""
Please enter your master password.
You can make everything faster with Google Authenticator! 
Press /g_auth_info

"""))
    else:
        await bot.send_message(chat_id, _("Enter the code from the app"))
    await Decode.MASTER_PASSWORD.set()


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def decode_start(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    file_id = message.document.file_id
    try:
        await bot.download_file_by_id(file_id, "to_decode.txt")
    except BadRequest:
        return await message.reply(_("INVALID FILE"))
    with open("to_decode.txt", "r") as file:
        try:
            text = file.read()
        except UnicodeDecodeError:
            await bot.send_message(chat_id, _("INVALID FILE"))
            return
    expression = re.compile(f"{Other_Texts.START}(.*){Other_Texts.END}")
    try:
        extract_encoded = expression.findall(text)[0]

    except IndexError:
        await bot.send_message(chat_id, _("Error. Wrong file"))
        return
    expression = re.compile(f"{Other_Texts.END}(.*){Other_Texts.END_CODE}")
    code = expression.findall(text)[0]
    await state.update_data(password=extract_encoded, code=code, doc=True)

    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, _("""
Please enter your master password.
You can make everything faster with Google Authenticator! 
Press /g_auth_info

"""))
    else:
        await bot.send_message(chat_id, _("Enter the code from the app"))
    await Decode.MASTER_PASSWORD.set()

    await asyncio.sleep(10)
    await message.delete()


@dp.message_handler(commands=["cancel"], state=Decode.MASTER_PASSWORD)
async def decode_1(message: types.Message, state: FSMContext):
    await message.answer("OK.")
    await dp.current_state().reset_state()


@dp.message_handler(state=Decode.MASTER_PASSWORD)
async def decode_1(message: types.Message, state: FSMContext):
    increase_message_counter()

    chat_id = message.chat.id
    en_password = (await state.get_data()).get("password")
    code = (await dp.current_state().get_data())["code"]
    if not enabled_g_auth(chat_id):
        master = message.text
    else:
        if not has_g_auth(chat_id):
            await message.reply(_("An error has occurred, you lost the Google authenticator settings\n"
                                  "Please re-configure it once again /g_auth_info"))
            await state.finish()

            return
        try:
            if verify(chat_id, message.text):
                master = get_google_auth(chat_id)
            else:
                await bot.send_message(chat_id, _("Code is incorrect, try again or /cancel"))
                return
        except binascii.Error:
            await bot.send_message(chat_id, _("Code is incorrect, try again or /cancel"))
            return

    password = (decode(master, en_password, code)).replace("\\n", "\n")

    if (await state.get_data()).get("doc"):

        with open("decoded.txt", "w") as file:
            file.write(password.replace("\\n", "\n"))
        await bot.send_document(chat_id, open("decoded.txt", "rb"))
        with open("decoded.txt", "w") as file:
            file.write(" ")
    else:
        await bot.send_message(chat_id, _("""
Your decoded password is inside citation marks '<code>{password}</code>'""").format(
            password=password
        ))
    await state.finish()

    await asyncio.sleep(10)
    await message.delete()

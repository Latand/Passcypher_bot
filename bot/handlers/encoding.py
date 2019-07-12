import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest

from app import bot, dp, _
from bot.aiogram_help.keyboard_maker import ListOfButtons
from bot.aiogram_help.states import Encode
from bot.utils.encode import encode
from bot.utils.google_auth import enabled_g_auth, get_google_auth
from bot.utils.some_functions import allowed_chars
from bot.utils.some_functions import increase_message_counter


@dp.message_handler(commands=["encode", "e"])
async def encode_start(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, _("""
Please enter your master password.
You can make everything faster with Google Authenticator! 
Press /g_auth_info

"""))
        await Encode.MASTER_PASSWORD.set()
    else:
        await state.update_data(master_pass=get_google_auth(chat_id))
        await Encode.PASSWORD.set()
        await bot.send_message(chat_id, _("""Enter phrase you want to encrypt.
It should be under 400 characters, for best results there should be only characters from this list:
<pre>{allowed_chars} </pre>
<b> THE BOT DELETES YOUR MESSAGES WITH PASSWORDS AFTER 10 SECONDS</b>
""").format(allowed_chars=allowed_chars))


@dp.callback_query_handler(text="encrypt_saved")
async def encode_saved(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    password_message = call.message.reply_to_message
    password = password_message.text
    await call.message.delete()
    async with state.proxy() as data:
        data["encrypt_from_saved"] = True
        data["to_encrypt"] = password

        await password_message.delete()

    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, _("""
Please enter your master password.
You can make everything faster with Google Authenticator! 
Press /g_auth_info

"""))
        await Encode.MASTER_PASSWORD.set()
    else:

        master_pass = get_google_auth(chat_id)

        if len(password) > 400:
            await bot.send_message(chat_id, _("Error has occurred... Too long phrase. Try to enter a phrase \
under 400 characters."))
            return
        elif not master_pass:
            await bot.send_message(chat_id, _("Master Password not found."))
            await state.finish()
            return

        text, code = encode(password.replace("\n", "\\n"), master_pass)
        hint = "Google Authenticator"
        await bot.send_message(chat_id, _("""<code>----------------------------
ENCRYPTION STARTS HERE
----------------------------
{passw}
----------------------------
ENCRYPTION ENDS HERE
----------------------------
CODE
{code}
----------------------------
</code>

Hint: {hint}
Save this message wherever you want and forward it to the bot should you need to decode it.
""").format(
            passw=text, code=code,
            hint=f"{hint}"
        ))
        await state.finish()
        increase_message_counter(password=True)

    await asyncio.sleep(10)


@dp.message_handler(state=Encode.MASTER_PASSWORD)
async def encoded(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    if "/g_auth_info" == message.text:
        text = _(
            "To encrypt your phrase/file you need to enter a master password each time you want to encrypt or decrypt, or"
            " you can enable <b>Google Authenticator</b> and enter one-time codes from your phone <b>only to decrypt</b>"
            "  your passwords. \n"
            "(Master password will be kept in database then) \n\n"
            "Please make your choice (you can change it later with command /reset_google_auth\n"
        )
        await bot.send_message(chat_id, text, reply_markup=ListOfButtons(
            text=[_("Setup")],
            callback=["g_auth_setup"]).inline_keyboard)
        await state.finish()
        return
    async with state.proxy() as data:
        data["master_pass"] = message.text

        password = data.get("to_encrypt")
        master_pass = data.get("master_pass")

    if not data.get("encrypt_from_saved"):
        await Encode.PASSWORD.set()
        await bot.send_message(chat_id, _("""Enter phrase you want to encrypt.
It should be under 400 characters, for best results there should be only characters from this list:
<pre>{allowed_chars} </pre>
<b> THE BOT DELETES YOUR MESSAGES WITH PASSWORDS AFTER 10 SECONDS</b>
""").format(allowed_chars=allowed_chars))
    else:
        if not password:
            await message.reply(_("Password not found."))
            await state.finish()
            return
        if len(password) > 400:
            await bot.send_message(chat_id, _("Error has occurred... Too long phrase. Try to enter a phrase under 400 \
characters."))
            await state.finish()
            return
        elif not master_pass:
            await message.reply(_("Master Password not found."))
            await state.finish()
            return

        text, code = encode(password.replace("\n", "\\n"), master_pass)
        if master_pass == get_google_auth(chat_id):
            hint = "Google Authenticator"
        else:
            hint = master_pass[:2] + "***********"
        await bot.send_message(chat_id, _("""<code>----------------------------
ENCRYPTION STARTS HERE
----------------------------
{passw}
----------------------------
ENCRYPTION ENDS HERE
----------------------------
CODE
{code}
----------------------------
</code>

Hint: {hint}
Save this message wherever you want and forward it to the bot should you need to decode it.
""").format(
            passw=text, code=code,
            hint=f"{hint}"
        ))
        await state.finish()
        increase_message_counter(password=True)

    await asyncio.sleep(10)
    await message.delete()


@dp.message_handler(state=Encode.PASSWORD, content_types=types.ContentType.TEXT)
async def encoded(message: types.Message, state: FSMContext):
    increase_message_counter(password=True)
    chat_id = message.chat.id
    master_pass = (await state.get_data()).get("master_pass")
    if len(message.text) > 400:
        await bot.send_message(chat_id, _("Error has occurred... Too long phrase. Try to enter a phrase under 400 \
characters."))
        return
    elif not master_pass:
        await message.reply(_("Master Password not found."))
        await state.finish()
        await asyncio.sleep(10)
        await message.delete()
        return
    text, code = encode(message.text.replace("\n", "\\n"), master_pass)
    if master_pass == get_google_auth(chat_id):
        hint = "Google Authenticator"
    else:
        hint = master_pass[:2] + "***********"
    await bot.send_message(chat_id, _("""<code>----------------------------
ENCRYPTION STARTS HERE
----------------------------
{passw}
----------------------------
ENCRYPTION ENDS HERE
----------------------------
CODE
{code}
----------------------------
</code>

Hint: {hint}
Save this message wherever you want and forward it to the bot should you need to decode it.
""").format(
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
    master_pass = (await state.get_data()).get("master_pass")
    file_id = message.document.file_id
    try:
        await bot.download_file_by_id(file_id, "to_encode.txt")
    except BadRequest:
        return await message.reply(_("INVALID FILE"))
    with open("to_encode.txt", "r") as file:
        try:
            text = file.read().replace("\n", "\\n")
        except UnicodeDecodeError:
            await bot.send_message(chat_id, _("INVALID FILE"))
            await state.finish()
            return

    text, code = encode(text, master_pass)
    with open("encoded.txt", "a") as file:
        file.write(_("""
----------------------------
ENCRYPTION STARTS HERE
----------------------------
{passw}
----------------------------
ENCRYPTION ENDS HERE
----------------------------
CODE
{code}
----------------------------
Hint: {hint}
""").format(
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

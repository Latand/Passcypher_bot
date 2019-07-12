from aiogram import types
from aiogram.dispatcher import FSMContext

from app import bot, dp, _
from bot.aiogram_help.filters import Buttons
from bot.aiogram_help.states import Encode
from bot.utils.google_auth import enabled_g_auth, get_google_auth, has_g_auth
from bot.utils.some_functions import increase_message_counter
from bot.aiogram_help.inline_button import ListOfButtons
from bot.utils.some_functions import allowed_chars


@dp.message_handler(Buttons("🔒 Encode"))
async def encode_m(message: types.Message, state: FSMContext):
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


@dp.message_handler(Buttons("🔑 Decode"))
async def decode_m(message: types.Message):
    increase_message_counter()

    await message.reply(_("https://telegra.ph/Passwords-Decryption-Process-06-02"))


@dp.message_handler(Buttons("ℹ️How to use"))
async def info_m(message: types.Message):
    increase_message_counter()
    await message.reply(_("https://telegra.ph/How-to-Use-Passcypher-Instruction-EN-06-02"))


@dp.message_handler(Buttons("🇬🇧 Set language"))
async def language_set(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    await bot.send_message(chat_id,
                           _("""
Hello, <b>{}</b>
Let's choose your language
""").format(message.from_user.first_name),
                           reply_markup=ListOfButtons(
                               text=["English", "Русский", "Українська"],
                               callback=["language en", "language ru", "language uk"]
                           ).inline_keyboard)


@dp.message_handler(Buttons("🔐 Two step verification"))
async def set_google_auth(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    text = _("https://telegra.ph/Passcypher-Google-Authenticator-06-02") + "\n\n"
    if has_g_auth(chat_id):
        if enabled_g_auth(chat_id):
            await bot.send_message(chat_id,
                                   text + _("Here you can enable and disable your Google Authenticator settings"),
                                   reply_markup=ListOfButtons(
                                       text=[_("Turn off")],
                                       callback=["turn 0"]).inline_keyboard)
        else:

            await bot.send_message(chat_id,
                                   text + _("Here you can enable and disable your Google Authenticator settings"),
                                   reply_markup=ListOfButtons(
                                       text=[_("Turn on")],
                                       callback=["turn 1"]).inline_keyboard)
    else:
        await bot.send_message(chat_id, _("Google Authenticator is not set for you. Press /g_auth_info"))

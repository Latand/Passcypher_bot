import binascii

from aiogram import types
from aiogram.dispatcher import FSMContext

from app import bot, dp, logging, _
from bot.aiogram_help.states import GoogleAuth
from bot.utils.google_auth import has_g_auth, enabled_g_auth, verify, create_google_auth
from bot.utils.some_functions import increase_message_counter, sql
from bot.aiogram_help.inline_button import ListOfButtons


@dp.message_handler(commands=["g_auth_info"])
async def info(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    text = _("""To encrypt your phrase/file you need to enter a master password each time you want to encrypt or decrypt, or\
 you can enable <b>Google Authenticator</b> and enter one-time codes from your phone <b>only to decrypt</b>\
  your passwords. \
(Master password will be kept in database then) 

Please make your choice (you can change it later with command /reset_google_auth
""")
    await bot.send_message(chat_id, text, reply_markup=ListOfButtons(
        text=[_("Setup")],
        callback=["g_auth_setup"]).inline_keyboard)


@dp.message_handler(commands=["reset_google_auth"])
async def info(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    if has_g_auth(chat_id):
        text = _("Here you can enable and disable your Google Authenticator settings")
        if enabled_g_auth(chat_id):
            await bot.send_message(chat_id, text,
                                   reply_markup=ListOfButtons(
                                       text=[_("Turn off")],
                                       callback=["turn 0"]).inline_keyboard)
        else:

            await bot.send_message(chat_id, text,
                                   reply_markup=ListOfButtons(
                                       text=[_("Turn on")],
                                       callback=["turn 1"]).inline_keyboard)
    else:
        await bot.send_message(chat_id, _("Google Authenticator is not set for you. Press /g_auth_info"))


@dp.callback_query_handler(text_contains="turn")
async def g_auth(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    enabled = call.data.split()[1]
    sql.update(table="users", enabled=enabled, condition={"chat_id": chat_id})
    try:
        await bot.edit_message_text(text=_("That is done"),
                                    chat_id=chat_id,
                                    message_id=call.message.message_id)
    except Exception as e:
        logging.error(f"{e}")


@dp.callback_query_handler(text="g_auth_setup")
async def g_auth(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    try:
        await bot.edit_message_reply_markup(chat_id, message_id=call.message.message_id)
    except Exception as e:
        logging.error(f"{e}")

    if has_g_auth(chat_id):
        await bot.send_message(chat_id, _("You have already received the Google Authenticator code"))
        return

    await bot.send_message(chat_id, _("""
Please ensure you have the app installed.
<a href= "https://itunes.apple.com/gb/app/google-authenticator/id388497605?mt=8">IOS</a>
<a href= "https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_GB">Android</a>

Press continue when you done. After you receive the code - write it down somewhere.
"""), reply_markup=ListOfButtons(
        text=[_("Continue")],
        callback=["continue"]).inline_keyboard)
    await GoogleAuth.ONE.set()


@dp.message_handler(commands=["cancel"], state=[GoogleAuth.TWO, GoogleAuth.ONE])
async def reset(message: types.Message, state: FSMContext):
    await state.reset_state()
    chat_id = message.chat.id

    sql.update(table="users", google="", enabled=0, condition={"chat_id": chat_id})
    await message.reply(_("That is done"))


@dp.message_handler(state=GoogleAuth.ONE)
async def g_auth(message: types.Message, state: FSMContext):
    await message.reply(_("Please press on button to continue or /cancel"))


@dp.callback_query_handler(state=GoogleAuth.ONE)
async def g_auth(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    try:
        await bot.edit_message_reply_markup(chat_id, message_id=call.message.message_id)
    except Exception as e:
        logging.error(f"{e}")
    if has_g_auth(chat_id):
        await bot.send_message(chat_id, _("You have already received the Google Authenticator code"))
        return

    code, link, qr_code = create_google_auth(chat_id)
    await bot.send_message(chat_id, _("""
You will receive a recovery code and a link below.
<b>IT WILL BE AUTOMATICALLY DELETED AFTER YOU CONFIRM</b>
"""))
    message_1 = (await bot.send_message(chat_id, code)).message_id

    message_2 = (await bot.send_photo(chat_id, qr_code,
                                      f"{link}")).message_id
    await bot.send_message(chat_id, _("Please enter the code from the Google Authenticator\n"
                                      "Pay attention that it updates every 30 sec."))

    await state.update_data(message_1=message_1, message_2=message_2)
    await GoogleAuth.next()


@dp.message_handler(state=GoogleAuth.TWO)
async def g_auth(message: types.Message, state: FSMContext):
    increase_message_counter()
    chat_id = message.chat.id
    try:
        ver = verify(chat_id, message.text)
    except binascii.Error:
        await bot.send_message(chat_id, _("Code is incorrect, try again or /cancel"))
        return
    if ver:
        async with state.proxy() as data:
            message_1 = data.get("message_1")
            message_2 = data.get("message_2")
        await bot.delete_message(chat_id, message_1)
        await bot.delete_message(chat_id, message_2)
        await bot.send_message(chat_id, _("Confirmation successful, you can proceed. /encode"))
        await state.finish()
    else:
        await bot.send_message(chat_id, _("Code is incorrect, try again or /cancel"))

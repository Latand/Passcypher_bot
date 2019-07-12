from aiogram import types
from aiogram.dispatcher.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities, MessageNotModified

from app import bot, dp, _
from bot.utils.some_functions import increase_message_counter, get_counters, check_if_new_user, set_language
from bot.aiogram_help.keyboard_maker import ListOfButtons


@dp.message_handler(commands=["start"], state="*")
async def starting(message: types.Message, state: FSMContext):
    increase_message_counter()
    await state.reset_state()
    chat_id = message.chat.id
    check_if_new_user(chat_id)

    menu = ListOfButtons(
        text=[_("🔒 Encode"),
              _("🔑 Decode"),
              _("ℹ️How to use"),
              _("🇬🇧 Set language"),
              _("🔐 Two step verification"),
              _("📝 Write a review")],
        align=[2, 2, 2]
    ).reply_keyboard

    await bot.send_message(chat_id,
                           _("""
Hello, <b>{}</b>
This bot is designed to encrypt your passwords so you can store them publicly, for example in your \
<code>Telegram saved messages.</code>

You can choose your language using command /set_language
""").format(message.from_user.first_name),
                           reply_markup=menu)


@dp.callback_query_handler(text_contains="language")
async def change_language(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    try:
        await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    except MessageNotModified:
        pass
    language = call.data.split()[1]
    set_language(chat_id, language)
    menu = ListOfButtons(
        text=[_("🔒 Encode", locale=language),
              _("🔑 Decode", locale=language),
              _("ℹ️How to use", locale=language),
              _("🇬🇧 Set language", locale=language),
              _("🔐 Two step verification", locale=language),
              _("📝 Write a review", locale=language)],
        align=[2, 2, 2]
    ).reply_keyboard

    await bot.send_message(chat_id, _("""Language has changed to 🇬🇧<b>EN</b>

<b>{users}</b> users are using this bot. 

<b>{passwords}</b> passwords encrypted.
<b>{messages}</b> messages received.

Start using this bot: /info""", locale=language).format(**get_counters()),
                           reply_markup=menu)


@dp.message_handler(commands=["statistics"])
async def statistics(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, _("""
<b>{users}</b> users are using this bot. 

<b>{passwords}</b> passwords encrypted.
<b>{messages}</b> messages received.
        """).format(**get_counters()))


@dp.message_handler(commands=["set_language"])
async def lang_choose(message: types.Message):
    chat_id = message.chat.id

    increase_message_counter()
    try:
        await bot.send_message(chat_id,
                               _("""
Hello, <b>{}</b>
Firstly, let's choose your language
""").format(message.from_user.first_name),
                               reply_markup=ListOfButtons(
                                   text=["English", "Русский", "Українська"],
                                   callback=["language en", "language ru", "language uk"]
                               ).inline_keyboard)
    except CantParseEntities as err:
        print(f"Error. CantParseEntities: {err}")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def unknown(message: types.Message, state: FSMContext):
    increase_message_counter()

    text = (_("🔒 Encode") + f" '{message.text}'")[:20] + "..."

    await message.reply(_("""
Looks like the input is invalid...
To decode your password - forward the message with encoded password you received from bot.
<a href= 'https://telegra.ph/file/a9f99684284a92eb2a6a0.png'>ᅠ</a>
Perhaps you wanted to encrypt this message? Click """) + _("🔒 Encode") +
                        _("\n\nOr setup the language again /set_language"),
                        reply_markup=ListOfButtons(
                            text=[text],
                            callback=[f"encrypt_saved"]
                        ).inline_keyboard)


@dp.message_handler(state="*")
async def unknown_message(message: types.Message, state: FSMContext):
    await message.reply(_("Seems like you have an unfinished business..."))


@dp.callback_query_handler(state="*")
async def unknown_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(_("Seems like you have an unfinished business..."))

from inline_button import *
from messages import texts as imported_text
from aiogram.utils.exceptions import CantParseEntities, MessageNotModified
from messages import Other_Texts, allowed_chars, get_text
from some_functions import *
from filters import *
from main_bot import bot, dp


@dp.message_handler(commands=["start"])
async def starting(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    await bot.send_message(chat_id,
                           Other_Texts.WELCOME_MESSAGE.format(message.from_user.first_name),
                           reply_markup=inlinemarkups(
                               text=["English", "Русский", "Українська"],
                               callback=["language en", "language ru", "language ua"]
                           ))


@dp.callback_query_handler(Callbacks("language", contains=True))
async def change_language(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    try:
        await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    except MessageNotModified:
        pass
    language = call.data.split()[1]
    set_language(chat_id, language)

    await bot.send_message(chat_id, get_text(language, "changed").format(**get_counters()),
                           reply_markup=menu(language))


@dp.message_handler(commands=["statistics"])
async def statistics(message: types.Message):
    chat_id = message.chat.id
    lang = get_language(chat_id)
    await bot.send_message(chat_id, get_text(lang, "stats").format(**get_counters()))


@dp.message_handler(commands=["set_language"])
async def lang_choose(message: types.Message):
    chat_id = message.chat.id

    increase_message_counter()
    try:
        await bot.send_message(chat_id,
                               Other_Texts.SET_LANGUAGE_MESSAGE.format(message.from_user.first_name),
                               reply_markup=inlinemarkups(
                                   text=["English", "Русский", "Українська"],
                                   callback=["language en", "language ru", "language ua"]
                               ))
    except CantParseEntities as err:
        print(f"Error. CantParseEntities: {err}")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def unknown(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    await bot.send_message(chat_id, get_text(lang, "OOPS"))

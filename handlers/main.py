from aiogram.utils.exceptions import CantParseEntities, MessageNotModified

from filters import *
from aiogram.dispatcher.dispatcher import FSMContext
from inline_button import *
from main_bot import bot, dp
from messages import Other_Texts
from some_functions import *
from inline_button import ListOfButtons


@dp.message_handler(commands=["start"], state="*")
async def starting(message: types.Message, state: FSMContext):
    increase_message_counter()
    await state.reset_state()
    chat_id = message.chat.id
    await bot.send_message(chat_id,
                           Other_Texts.WELCOME_MESSAGE.format(message.from_user.first_name),
                           reply_markup=ListOfButtons(
                               text=["English", "Русский", "Українська"],
                               callback=["language en", "language ru", "language ua"]
                           ).inline_keyboard)


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


@dp.message_handler(commands=["set_language"])111
async def lang_choose(message: types.Message):
    chat_id = message.chat.id

    increase_message_counter()
    try:
        await bot.send_message(chat_id,
                               Other_Texts.SET_LANGUAGE_MESSAGE.format(message.from_user.first_name),
                               reply_markup=ListOfButtons(
                                   text=["English", "Русский", "Українська"],
                                   callback=["language en", "language ru", "language ua"]
                               ).inline_keyboard)
    except CantParseEntities as err:
        print(f"Error. CantParseEntities: {err}")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def unknown(message: types.Message, state: FSMContext):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = (get_text(lang, "ENCODE") + f" '{message.text}'")[:20] + "..."

    await message.reply(get_text(lang, "OOPS"),
                        reply_markup=ListOfButtons(
                            text=[text],
                            callback=[f"encrypt_saved"]
                        ).inline_keyboard)


@dp.message_handler(state="*")
async def unknown_message(message: types.Message, state: FSMContext):
    await message.reply("Seems like you have an unfinished business...")


@dp.callback_query_handler(state="*")
async def unknown_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Seems like you have an unfinished business...")

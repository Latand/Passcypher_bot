import asyncio
import logging
import config
import aiogram
from inline_button import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from languages import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
from messages import texts as imported_text
from states import ALL_STATES as STATE
from encode import encode
from decode import decode
import re
from messages import Other_Texts, allowed_chars
from google_auth import *
import binascii
from some_functions import *

WEBHOOK_PATH = f'/{config.TOKEN}'
WEBHOOK_URL = f"https://{config.WEBHOOK_HOST}{WEBHOOK_PATH}/"

# webserver settings
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = config.PORT

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, loop=loop, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def starting(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    await bot.send_message(chat_id,
                           Other_Texts.WELCOME_MESSAGE.format(message.from_user.first_name),
                           reply_markup=inlinemarkups(
                               text=["English", "Русский"],
                               callback=["language en start", "language ru start"]
                           ))


@dp.callback_query_handler(func=lambda call: "language" in call.data)
async def change_language(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    try:
        await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    except aiogram.utils.exceptions.MessageNotModified:
        pass
    language = call.data.split()[1]
    set_language(chat_id, language)

    await bot.send_message(chat_id, imported_text[language]["changed"].format(**get_counters()),
                           reply_markup=menu(language))


@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = imported_text[lang]["describe en 1"]
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[imported_text[lang]["next"]],
        callback=["describe_en 2"]
    ))
    text = imported_text[lang]["describe de 1"]
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[imported_text[lang]["next"]],
        callback=["describe_de 2"]
    ))


# SETUP GOOGLE AUTH ----------------------------------------------------------------------------------------


@dp.message_handler(commands=["g_auth_info"])
async def info(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = imported_text[lang]["g_auth info"]
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[imported_text[lang]["enable_g_auth"]],
        callback=["g_auth_setup"]))


@dp.message_handler(commands=["reset_google_auth"])
async def info(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    if has_g_auth(chat_id):
        if enabled_g_auth(chat_id):
            await bot.send_message(chat_id, imported_text[lang]["reset gauth"], reply_markup=inlinemarkups(
                text=[imported_text[lang]["turn off"]],
                callback=["turn 0"]))
        else:

            await bot.send_message(chat_id, imported_text[lang]["reset gauth"], reply_markup=inlinemarkups(
                text=[imported_text[lang]["turn on"]],
                callback=["turn 1"]))
    else:
        await bot.send_message(chat_id, imported_text[lang]["not set"])


@dp.callback_query_handler(func=lambda call: "turn" in call.data)
async def g_auth(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    sql.update(table="users", enabled=call.data.split()[1], condition={"chat_id": chat_id})
    try:
        await bot.edit_message_text(text=imported_text[lang]["done"], chat_id=chat_id,
                                    message_id=call.message.message_id)
    except Exception:
        pass


@dp.callback_query_handler(func=lambda call: "g_auth_setup" == call.data)
async def g_auth(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    try:
        await bot.edit_message_reply_markup(chat_id, message_id=call.message.message_id)
    except Exception:
        pass

    if has_g_auth(chat_id):
        await bot.send_message(chat_id, imported_text[lang]["already enabled"])
        return

    await bot.send_message(chat_id, imported_text[lang]["google_auth setup 1"], reply_markup=inlinemarkups(
        text=[imported_text[lang]["continue"]],
        callback=["continue"]))
    await dp.current_state().set_state(STATE.G_AUTH_1)


@dp.callback_query_handler(state=STATE.G_AUTH_1)
async def g_auth(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    try:
        await bot.edit_message_reply_markup(chat_id, message_id=call.message.message_id)
    except Exception:
        pass
    if has_g_auth(chat_id):
        await bot.send_message(chat_id, imported_text[lang]["already enabled"])
        return

    code, link, qr_code = create_google_auth(chat_id)
    await bot.send_message(chat_id, imported_text[lang]["google_auth setup 2"])
    message_1 = (await bot.send_message(chat_id, code)).message_id

    message_2 = (await bot.send_photo(chat_id, qr_code,
                                      f"{link}")).message_id
    await bot.send_message(chat_id, imported_text[lang]["google_auth setup 3"])

    await dp.current_state().update_data(message_1=message_1, message_2=message_2)
    await dp.current_state().set_state(STATE.G_AUTH_2)


@dp.message_handler(state=STATE.G_AUTH_2)
async def g_auth(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    try:
        ver = verify(chat_id, message.text)
    except binascii.Error:
        await bot.send_message(chat_id, imported_text[lang]["invalid code"])
        return
    if ver:
        message_1 = (await dp.current_state().get_data()).get("message_1")
        message_2 = (await dp.current_state().get_data()).get("message_2")
        await bot.delete_message(chat_id, message_1)
        await bot.delete_message(chat_id, message_2)
        await bot.send_message(chat_id, imported_text[lang]["confirm yes"])
        await dp.current_state().reset_state()
    else:
        await bot.send_message(chat_id, imported_text[lang]["confirm no"])
        return


# SETUP GOOGLE AUTH ----------------------------------------------------------------------------------------

# DESCRIBE BOT ---------------------------------------------------------------------------------------------


@dp.callback_query_handler(func=lambda call: "describe_en" in call.data)
async def next_page(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    page = int(call.data.split()[1])
    buts, calls = [], []
    if page > 1:
        buts.append(imported_text[lang]["prev"])
        calls.append(f"describe_en {page-1}")
    if page < 4:
        buts.append(imported_text[lang]["next"])
        calls.append(f"describe_en {page+1}")
    await bot.edit_message_text(chat_id=chat_id, text=imported_text[lang][f"describe en {page}"].format(
        allowed_chars=allowed_chars),
                                message_id=call.message.message_id,
                                reply_markup=inlinemarkups(
                                    text=buts,
                                    callback=calls,
                                    align=[len(buts)]
                                ))


@dp.callback_query_handler(func=lambda call: "describe_de" in call.data)
async def next_page(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    page = int(call.data.split()[1])
    buts, calls = [], []
    if page > 1:
        buts.append(imported_text[lang]["prev"])
        calls.append(f"describe_de {page-1}")
    if page < 3:
        buts.append(imported_text[lang]["next"])
        calls.append(f"describe_de {page+1}")
    await bot.edit_message_text(chat_id=chat_id, text=imported_text[lang][f"describe de {page}"],
                                message_id=call.message.message_id,
                                reply_markup=inlinemarkups(
                                    text=buts,
                                    callback=calls,
                                    align=[len(buts)]
                                ))


# DESCRIBE BOT ---------------------------------------------------------------------------------------------


@dp.message_handler(commands=["set_language"])
async def lang_choose(message: types.Message):
    chat_id = message.chat.id

    increase_message_counter()
    try:
        await bot.send_message(chat_id,
                               Other_Texts.SET_LANGUAGE_MESSAGE.format(message.from_user.first_name),
                               reply_markup=inlinemarkups(
                                   text=["English", "Русский"],
                                   callback=["language en", "language ru"]
                               ))
    except aiogram.utils.exceptions.CantParseEntities as err:
        print(f"Error. {err.__class__.__name__}: {err}")


# ENCODE PROCESS---------------------------------------------------------------------------------------------
@dp.message_handler(commands=["encode", "e"])
async def encode_start(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, imported_text[lang]["encode master"])
        await dp.current_state().set_state(STATE.MASTER_ENCODE)
    else:
        await dp.current_state().update_data(master_pass=get_google_auth(chat_id))
        await dp.current_state().set_state(STATE.PASSWORD_ENCODE)
        await bot.send_message(chat_id, imported_text[lang]["password"].format(allowed_chars=allowed_chars))


@dp.message_handler(state=STATE.MASTER_ENCODE)
async def encoded(message: types.Message):
    increase_message_counter()
    chat_id = message.chat.id
    lang = get_language(chat_id)
    if "/g_auth_info" == message.text:
        text = imported_text[lang]["g_auth info"]
        await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
            text=[imported_text[lang]["enable_g_auth"]],
            callback=["g_auth_setup"]))
        await dp.current_state().reset_state()
        return
    await dp.current_state().update_data(master_pass=message.text)
    await dp.current_state().set_state(STATE.PASSWORD_ENCODE)
    await bot.send_message(chat_id, imported_text[lang]["password"].format(allowed_chars=allowed_chars))


@dp.message_handler(state=STATE.PASSWORD_ENCODE, content_types=types.ContentType.TEXT)
async def encoded(message: types.Message):
    increase_message_counter(password=True)
    chat_id = message.chat.id
    lang = get_language(chat_id)
    master_pass = (await dp.current_state().get_data())["master_pass"]
    if len(message.text) > 400:
        await bot.send_message(chat_id, imported_text[lang]["large"])
        return
    text, code = encode(message.text.replace("\n", "\\n"), master_pass)
    await bot.send_message(chat_id, imported_text[lang]["result_encode"].format(
        passw=text, code=code,
        hint=f"{master_pass[:2]}***********"
    ))
    await dp.current_state().reset_state()


@dp.message_handler(state=STATE.PASSWORD_ENCODE, content_types=types.ContentType.DOCUMENT)
async def encoded(message: types.Message):
    increase_message_counter(password=True)
    chat_id = message.chat.id
    lang = get_language(chat_id)
    master_pass = (await dp.current_state().get_data())["master_pass"]
    file_id = message.document.file_id
    await bot.download_file_by_id(file_id, "to_encode.txt")
    with open("to_encode.txt", "r") as file:
        try:
            text = file.read().replace("\n", "\\n")
        except UnicodeDecodeError:
            await bot.send_message(chat_id, "INVALID FILE")
            await dp.current_state().reset_state()
            return

    text, code = encode(text, master_pass)
    with open("encoded.txt", "a") as file:
        file.write(imported_text[lang]["result_encode_doc"].format(
            passw=text, code=code,
            hint=f"{master_pass[:2]}***********"))
    await bot.send_document(chat_id, open("encoded.txt", "rb"))

    with open("encoded.txt", "w") as file:
        file.write(" ")

    with open("to_encode.txt", "w") as file:
        file.write(" ")
    await dp.current_state().reset_state()


# ENCODE PROCESS---------------------------------------------------------------------------------------------

# DECODE PROCESS---------------------------------------------------------------------------------------------


@dp.message_handler(regexp="#encoded_pass")
async def decode_start(message: types.Message):
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
    await dp.current_state().update_data(password=encoded, code=code)
    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, imported_text[lang]["encode master"])
    else:
        await bot.send_message(chat_id, imported_text[lang]["g_auth decode"])
    await dp.current_state().set_state(STATE.MASTER_DECODE)


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def decode_start(message: types.Message):
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
    expression = f"{Other_Texts.START}(.*){Other_Texts.END}"
    try:
        extract_encoded = re.findall(expression, text)[0]
    except IndexError:
        await bot.send_message(chat_id, "Error. Wrong file")
        return
    expression = f"{Other_Texts.END}(.*){Other_Texts.END_CODE}"
    code = re.findall(expression, text)[0]
    await dp.current_state().update_data(password=extract_encoded, code=code, doc=True)

    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, imported_text[lang]["encode master"])
    else:
        await bot.send_message(chat_id, imported_text[lang]["g_auth decode"])
    await dp.current_state().set_state(STATE.MASTER_DECODE)


@dp.message_handler(state=STATE.MASTER_DECODE)
async def decode_1(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    en_password = (await dp.current_state().get_data())["password"]
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
                await bot.send_message(chat_id, imported_text[lang]["invalid code"])
                return
        except binascii.Error:
            await bot.send_message(chat_id, imported_text[lang]["invalid code"])
            return

    password = (decode(master, en_password, code)).replace("\\n", "\n")

    if (await dp.current_state().get_data()).get("doc"):

        with open("decoded.txt", "w") as file:
            file.write(password.replace("\\n", "\n"))
        await bot.send_document(chat_id, open("decoded.txt", "rb"))
        with open("decoded.txt", "w") as file:
            file.write(" ")
    else:
        await bot.send_message(chat_id, imported_text[lang]["decoded_result"].format(
            password=password
        ))
    await dp.current_state().reset_state()


# DECODE PROCESS---------------------------------------------------------------------------------------------


# GOOGLE AUTH SETUP PROCESS----------------------------------------------------------------------------------


@dp.message_handler(func=lambda m: m.text in ENCODE.values())
async def encode_m(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    if not enabled_g_auth(chat_id):
        await bot.send_message(chat_id, imported_text[lang]["encode master"])
        await dp.current_state().set_state(STATE.MASTER_ENCODE)
    else:
        await dp.current_state().update_data(master_pass=get_google_auth(chat_id))
        await dp.current_state().set_state(STATE.PASSWORD_ENCODE)
        await bot.send_message(chat_id, imported_text[lang]["password"].format(allowed_chars=allowed_chars))


@dp.message_handler(func=lambda m: m.text in DECODE.values())
async def decode_m(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = imported_text[lang]["describe de 1"]
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[imported_text[lang]["next"]],
        callback=["describe_de 2"]
    ))


@dp.message_handler(func=lambda m: m.text in INFO.values())
async def info_m(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = imported_text[lang]["describe en 1"]
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[imported_text[lang]["next"]],
        callback=["describe_en 2"]
    ))
    text = imported_text[lang]["describe de 1"]
    await bot.send_message(chat_id, text, reply_markup=inlinemarkups(
        text=[imported_text[lang]["next"]],
        callback=["describe_de 2"]
    ))


@dp.message_handler(func=lambda m: m.text in LANGUAGE.values())
async def language_set(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    await bot.send_message(chat_id,
                           Other_Texts.SET_LANGUAGE_MESSAGE.format(message.from_user.first_name),
                           reply_markup=inlinemarkups(
                               text=["English", "Русский"],
                               callback=["language en", "language ru"]
                           ))


@dp.message_handler(func=lambda m: m.text in GOOGLE_AUTH.values())
async def set_google_auth(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    if has_g_auth(chat_id):
        if enabled_g_auth(chat_id):
            await bot.send_message(chat_id, imported_text[lang]["reset gauth"], reply_markup=inlinemarkups(
                text=[imported_text[lang]["turn off"]],
                callback=["turn 0"]))
        else:

            await bot.send_message(chat_id, imported_text[lang]["reset gauth"], reply_markup=inlinemarkups(
                text=[imported_text[lang]["turn on"]],
                callback=["turn 1"]))
    else:
        await bot.send_message(chat_id, imported_text[lang]["not set"])


# -------------------------------------------------------------- REVIEW SECTION (DELETE IF NOT USED)
@dp.message_handler(func=lambda m: m.text in REVIEWS.values())
async def set_google_auth(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    await bot.send_message(chat_id, imported_text[lang]["advice"],
                           reply_markup=inlinemarkups(
                               text=[imported_text[lang]["g_advice"]],
                               callback=["give_advice"]
                           ))


@dp.callback_query_handler(func=lambda call: "give_advice" == call.data)
async def next_page(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    await dp.current_state().set_state(STATE.REVIEW)
    await bot.edit_message_reply_markup(chat_id, call.message.message_id)
    last_message = await bot.send_message(chat_id, imported_text[lang]["adv_message"].format(advice=" "),
                                          reply_markup=inlinemarkups(
                                              text=[imported_text[lang]["cancel"]],
                                              callback=["cancel"]
                                          ))
    await dp.current_state().update_data(last_message=last_message.message_id)


@dp.message_handler(state=STATE.REVIEW)
async def set_google_auth(message: types.Message):
    chat_id = message.chat.id
    lang = get_language(chat_id)
    try:
        last_message = (await dp.current_state().get_data()).get("last_message")
        await bot.edit_message_reply_markup(chat_id, last_message)
    except:
        pass
    await dp.current_state().update_data(advice=message.text)
    last_message = await bot.send_message(chat_id, imported_text[lang]["adv_message"].format(advice=message.text),
                                          reply_markup=inlinemarkups(
                                              text=[
                                                  imported_text[lang]["send_adv"],
                                                  imported_text[lang]["cancel"]],
                                              callback=[
                                                  "publish",
                                                  "cancel"]
                                          ))

    await dp.current_state().update_data(last_message=last_message.message_id)


@dp.callback_query_handler(state=STATE.REVIEW)
async def next_page(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)

    try:
        last_message = (await dp.current_state().get_data()).get("last_message")
        await bot.edit_message_reply_markup(chat_id, last_message)
    except:
        pass

    if call.data == "cancel":
        await bot.send_message(chat_id, imported_text[lang]["cancelled"])
        await dp.current_state().reset_state()
        return
    elif call.data == "publish":
        if await throttling_message(chat_id):
            return
        advice = (await dp.current_state().get_data()).get("advice")
        await bot.send_message(config.review_channel, imported_text[lang]["post_advice"].format(advice))
# -------------------------------------------------------------- REVIEW SECTION (DELETE IF NOT USED)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def unknown(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    await bot.send_message(chat_id, imported_text[lang]["OOPS"])


async def throttling_message(user):
    try:
        await dp.throttle(str(user), rate=1)
    except Throttled:
        await bot.send_message(user, "Too fast. Try again in 1 sec")
        return True


async def on_startup(dp):
    return await bot.set_webhook(url=WEBHOOK_URL)


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path="",
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT, on_startup=on_startup)

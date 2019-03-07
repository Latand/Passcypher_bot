from some_functions import *
from inline_button import *
from main_bot import bot, dp, logging, throttling_message
from states import *
from filters import *
from aiogram.dispatcher import FSMContext
import config


@dp.message_handler(Buttons("REVIEWS"))
async def reviews_button(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    lang = get_language(chat_id)
    await bot.send_message(chat_id, get_text(lang, "advice"),
                           reply_markup=inlinemarkups(
                               text=[get_text(lang, "g_advice")],
                               callback=["give_advice"]
                           ))


@dp.callback_query_handler(Callbacks("give_advice"))
async def give_advice(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)
    await Other.REVIEW.set()
    await bot.edit_message_reply_markup(chat_id, call.message.message_id)
    last_message = await bot.send_message(chat_id, get_text(lang, "adv_message").format(advice=" "),
                                          reply_markup=inlinemarkups(
                                              text=[get_text(lang, "cancel")],
                                              callback=["cancel"]
                                          ))
    await state.update_data(last_message=last_message.message_id)


@dp.message_handler(state=Other.REVIEW)
async def your_advice(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    lang = get_language(chat_id)
    try:
        last_message = (await state.get_data()).get("last_message")
        await bot.edit_message_reply_markup(chat_id, last_message)
    except Exception as e:
        logging.error(f"{e}")
    await state.update_data(advice=message.text)
    last_message = await bot.send_message(chat_id, get_text(lang, "adv_message").format(advice=message.text),
                                          reply_markup=inlinemarkups(
                                              text=[
                                                  get_text(lang, "send_adv"),
                                                  get_text(lang, "cancel")],
                                              callback=[
                                                  "publish",
                                                  "cancel"]
                                          ))

    await state.update_data(last_message=last_message.message_id)


@dp.callback_query_handler(state=Other.REVIEW)
async def cancel_or_publish(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    lang = get_language(chat_id)

    try:
        last_message = (await state.get_data()).get("last_message")
        await bot.edit_message_reply_markup(chat_id, last_message)
    except Exception as e:
        logging.error(f"{e}")

    if call.data == "cancel":
        await bot.send_message(chat_id, get_text(lang, "cancelled"))
        await state.finish()
        return
    elif call.data == "publish":
        if await throttling_message(chat_id):
            return
        advice = (await state.get_data()).get("advice")
        await bot.send_message(config.review_channel, get_text(lang, "post_advice").format(advice))

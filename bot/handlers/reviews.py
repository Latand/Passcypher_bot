from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from bot.load_all import bot, dp, logging, _
from bot.aiogram_help.filters import Buttons
from bot.aiogram_help.states import Other
from bot.utils.some_functions import increase_message_counter
from bot.aiogram_help.keyboard_maker import ListOfButtons


@dp.message_handler(Buttons("📝 Write a review"))
async def reviews_button(message: types.Message):
    increase_message_counter()

    chat_id = message.chat.id
    await bot.send_message(chat_id, _("""Please, it is important for me to receive a response and advice from you.
How would you change the bot? Any comments are appreciated. 

Your comment will be posted <b>anonymously</b> in our channel @pcypher
Or you can just rate the bot using this link: https://t.me/pcypher/16
"""),
                           reply_markup=ListOfButtons(
                               text=[_("Give an advice to the bot")],
                               callback=["give_advice"]
                           ).inline_keyboard)


@dp.callback_query_handler(text="give_advice")
async def give_advice(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    await Other.REVIEW.set()
    await bot.edit_message_reply_markup(chat_id, call.message.message_id)
    last_message = await bot.send_message(chat_id, _("""
Your advice: 

{advice}

Write your advice in the next message.
""").format(advice=" "),
                                          reply_markup=ListOfButtons(
                                              text=[_("Cancel")],
                                              callback=["cancel"]
                                          ).inline_keyboard)
    await state.update_data(last_message=last_message.message_id)


@dp.message_handler(state=Other.REVIEW)
async def your_advice(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    try:
        last_message = (await state.get_data()).get("last_message")
        await bot.edit_message_reply_markup(chat_id, last_message)
    except Exception as e:
        logging.error(f"{e}")
    await state.update_data(advice=message.text)
    last_message = await bot.send_message(chat_id, _("""
Your advice: 

{advice}

Write your advice in the next message.
""").format(advice=message.text),
                                          reply_markup=ListOfButtons(
                                              text=[
                                                  _("Publish"),
                                                  _("Cancel")],
                                              callback=[
                                                  "publish",
                                                  "cancel"]
                                          ).inline_keyboard)

    await state.update_data(last_message=last_message.message_id)


@dp.callback_query_handler(state=Other.REVIEW)
async def cancel_or_publish(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    try:
        last_message = (await state.get_data()).get("last_message")
        await bot.edit_message_reply_markup(chat_id, last_message)
    except Exception as e:
        logging.error(f"{e}")

    if call.data == "cancel":
        await bot.send_message(chat_id, _("Cancelled"))
        await state.finish()
        return
    elif call.data == "publish":
        advice = (await state.get_data()).get("advice")
        await bot.send_message(config.review_channel, _("""
#Reviews Post:

<b>{}</b>
""").format(advice))

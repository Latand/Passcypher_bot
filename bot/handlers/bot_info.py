from aiogram import types

from bot.load_all import dp, _
from bot.utils.some_functions import increase_message_counter


@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    increase_message_counter()
    await message.reply(_("https://telegra.ph/How-to-Use-Passcypher-Instruction-EN-06-02"))

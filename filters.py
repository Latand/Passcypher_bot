from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from languages import *
from messages import get_text


class Buttons(BoundFilter):
    def __init__(self, key):
        self.key = key

    async def check(self, message: types.Message):
        chat_id = message.chat.id
        language = get_language(chat_id)
        return message.text == get_text(language, self.key)


class Callbacks(BoundFilter):
    def __init__(self, key, contains=False):
        self.key = key
        self.contains = contains

    async def check(self, call: types.CallbackQuery):
        if self.contains:
            return self.key in call.data

        return self.key == call.data

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app import _
from config import admin_id


class Buttons(BoundFilter):
    def __init__(self, key):
        self.key = key

    async def check(self, message: types.Message):
        return _(self.key) == message.text


class Callbacks(BoundFilter):
    def __init__(self, key, contains=False):
        self.key = key
        self.contains = contains

    async def check(self, call: types.CallbackQuery):
        if self.contains:
            return self.key in call.data

        return self.key == call.data


class IsAdmin(BoundFilter):
    admin_id = admin_id

    def __init__(self):
        pass

    async def check(self, message: types.Message):
        return message.chat.id == self.admin_id

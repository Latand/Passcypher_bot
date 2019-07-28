from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from load_all import _
from config import admin_id


class Buttons(BoundFilter):
    def __init__(self, key):
        self.key = key

    async def check(self, message: types.Message):
        return _(self.key) == message.text


class IsAdmin(BoundFilter):
    admin_id = admin_id

    def __init__(self):
        pass

    async def check(self, message: types.Message):
        return message.chat.id == self.admin_id

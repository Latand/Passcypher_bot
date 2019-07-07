from aiogram.dispatcher.filters.state import State, StatesGroup


class Encode(StatesGroup):
    MASTER_PASSWORD = State()
    PASSWORD = State()
    CODE = State()


class Decode(StatesGroup):
    MASTER_PASSWORD = State()
    PASSWORD = State()
    CODE = State()


class Other(StatesGroup):
    REVIEW = State()


class GoogleAuth(StatesGroup):
    ONE = State()
    TWO = State()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from messages import texts

def inlinemarkups(**kwargs) -> InlineKeyboardMarkup:
    keybd = InlineKeyboardMarkup()
    text = kwargs["text"]
    callback = kwargs["callback"]
    if "align" not in kwargs or kwargs["align"] is None:
        for button in range(len(kwargs["text"])):
            keybd.add(
                InlineKeyboardButton(
                    text=kwargs["text"][button],
                    callback_data=kwargs["callback"][button]
                )
            )
    else:
        for row in kwargs["align"]:
            rows = []
            for _ in range(row):
                try:
                    rows.append(InlineKeyboardButton(text=text.pop(0),
                                                     callback_data=callback.pop(0)))
                except:
                    print("Wrong align!")
            keybd.row(*rows)
    return keybd


def commmarkups(buts: list(), align: list() = ()) -> ReplyKeyboardMarkup:
    keybd = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    if not align:
        if isinstance(buts, str):
            buts = [buts]
        for text in buts:
            keybd.add(KeyboardButton(str(text)))
    else:
        for rows in align:
            row = []
            for text in range(rows):
                row.append(KeyboardButton(str(buts.pop(0))))
            keybd.add(*row)
    return keybd


ENCODE = {
    "ru": "🔒Зашифровать",
    "en": "🔒Encode"
}
DECODE = {
    "ru": "🔑Расшифровать",
    "en": "🔑Decode"
}
INFO = {
    "ru": "ℹ️Как использовать",
    "en": "ℹ️How to use"
}
LANGUAGE = {
    "ru": "🇷🇺Сменить язык",
    "en": "🇬🇧Set language"
}
GOOGLE_AUTH = {
    "ru": "🔐Двухэтапная верификация",
    "en": "🔐Two step verification"
}


def menu(lang):
    return commmarkups(
        buts=[ENCODE[lang], DECODE[lang],
              INFO[lang], LANGUAGE[lang],
              GOOGLE_AUTH[lang]],
        align=[2, 2, 1]
    )

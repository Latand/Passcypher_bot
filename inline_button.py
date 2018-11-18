from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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


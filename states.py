from aiogram.utils.helper import Helper, HelperMode, Item


class ALL_STATES(Helper):
    mode = HelperMode.snake_case

    MASTER_ENCODE = Item()
    MASTER_DECODE = Item()

    PASSWORD_ENCODE = Item()
    PASSWORD_DECODE = Item()

    CODE_DECODE = Item()
    KEY_DECODE = Item()








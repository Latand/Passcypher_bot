from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types
from config import I18N_DOMAIN, LOCALES_DIR
from bot.utils.some_functions import sql


def get_lang(chat_id):
    return sql.select(what="language", where="users", condition={"chat_id": chat_id})


class ACLMiddleware(I18nMiddleware):
    """
    Modified i18n middleware
    """

    async def get_user_locale(self, action, args):
        user = types.User.get_current()
        return get_lang(user.id) or user.locale


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)

    dp.middleware.setup(i18n)
    return i18n

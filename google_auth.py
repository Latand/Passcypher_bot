import pyotp
import pyqrcode
import os
from sql import sql


def create_google_auth(chat_id: int):
    code = pyotp.random_base32()
    link = f"otpauth://totp/{chat_id}%20%40%20Passcypher?secret={code}"
    qr = pyqrcode.create(link, "L")
    name = f"code_{chat_id}.png"
    qr.png(name, scale=6)
    with open(name, "rb") as file:
        qr_code = file.read()

    os.remove(name)

    sql.update(table="users", google=code, enabled=1, condition={"chat_id": chat_id})
    return code, link, qr_code


def enabled_g_auth(chat_id):
    return sql.select(what="enabled", where="users", condition={"chat_id": chat_id})


def has_g_auth(chat_id):
    return sql.select(what="google", where="users", condition={"chat_id": chat_id}) is not None


def verify(chat_id, code: int):
    totp = pyotp.TOTP(sql.select(where="users",
                                 what="google",
                                 condition={"chat_id": chat_id}))
    return totp.verify(str(code))


def get_google_auth(chat_id):
    return sql.select(where="users",
                      what="google",
                      condition={"chat_id": chat_id})

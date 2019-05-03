import os

import pyotp
import pyqrcode
import re
from sql import sql
import logging


def create_google_auth(chat_id: int):
    code = pyotp.random_base32()
    link = f"otpauth://totp/bot:{chat_id}@Passcypher?secret={code}&issuer=Passcypher"
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
    return sql.select(what="google", where="users", condition={"chat_id": chat_id})


def verify(chat_id, code: str):
    if not code:
        return False
    secret = get_google_auth(chat_id)
    if not secret:
        return False
    totp = pyotp.TOTP(secret)
    code_regex = re.compile(r"^(\d{3}).?(\d{3})")
    code = code_regex.findall(code)
    if not code:
        return False
    code = "".join(*code)
    if not code:
        return False
    return totp.verify(code)


def get_google_auth(chat_id):
    return sql.select(where="users",
                      what="google",
                      condition={"chat_id": chat_id})


def insert_dash(line):
    return "-".join([line[i:i + 4] for i in range(0, len(line), 4)])

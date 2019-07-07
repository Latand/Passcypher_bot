from bot.utils.sql import sql


def increase_message_counter(password=False):
    sql.update(table="Statistics", messages="`messages`+1", condition={"id": 0}, raw=True)
    if password:
        sql.update(table="Statistics", passwords="`passwords`+1", condition={"id": 0}, raw=True)


def get_counters():
    users = sql.select(what="COUNT(*)", where="users")
    messages, passwords = sql.select(where="Statistics", what=["messages", "passwords"], condition={"id": 0})[0]
    return {"users": users, "messages": messages, "passwords": passwords}


allowed_chars = 'qwertyuiopasdfghjklzxcvbnm,.!£$%^&*()[];_-+1234567890йцукенгшщзхъфывапролджэячсмитьбю'
to_mix = 'qwertyuiop asdfghjklzxcvbnm,.!£$%^&*()[];_-+1234567890 йцукенгшщзхъфывапролджэячсмитьбю'


class OtherTexts:
    START = """----------------------------
ENCRYPTION STARTS HERE
----------------------------
"""
    END = """
----------------------------
ENCRYPTION ENDS HERE
----------------------------
CODE
"""
    END_CODE = """
----------------------------"""


def set_language(chat_id, lang):
    sql.update(table="users", language=lang, condition={"chat_id": chat_id})


def check_if_new_user(chat_id):
    if not sql.select(where="users", condition={"chat_id": chat_id}):
        sql.insert(table="users", chat_id=chat_id)

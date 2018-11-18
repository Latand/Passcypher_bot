from sql import sql


def get_language(chat_id):
    if chat_id in people:
        return people[chat_id]
    else:
        language = sql.select(what="language", where="users", condition={"chat_id": chat_id})
        if language != ():
            people[chat_id] = language
            return language
        else:
            return "ru"


def set_language(chat_id, language):
    if chat_id not in people:
        if sql.select(what="COUNT(*)", where="users", condition={"chat_id": chat_id}) == 0:
            sql.insert(table="users", chat_id=chat_id, language=language)
            people[chat_id] = language
    else:
        sql.update(table="users", language=language, condition={"chat_id": chat_id})
        people[chat_id] = language


people = {}

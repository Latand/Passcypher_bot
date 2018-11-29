from sql import sql


def increase_message_counter(password=False):
    sql.update(table="Statistics", messages="messages+1")
    if password:
        sql.update(table="Statistics", passwords="passwords+1")


def get_counters():
    users = sql.select(what="COUNT(*)", where="users")
    messages, passwords = sql.select(where="Statistics", what=["messages", "passwords"])[0]
    return {"users": users, "messages": messages, "passwords": passwords}


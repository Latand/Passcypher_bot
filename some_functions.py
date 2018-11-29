from sql import sql


def increase_message_counter(password=False):
    sql.update(table="Statistics", messages="`messages`+1", condition={"id": 0}, raw=True)
    if password:
        sql.update(table="Statistics", passwords="`passwords`+1", condition={"id": 0}, raw=True)


def get_counters():
    users = sql.select(what="COUNT(*)", where="users")
    messages, passwords = sql.select(where="Statistics", what=["messages", "passwords"], condition={"id": 0})[0]
    return {"users": users, "messages": messages, "passwords": passwords}


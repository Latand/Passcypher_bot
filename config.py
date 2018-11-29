import os

TOKEN = os.environ.get("BOT_TOKEN_CYPHER")
WEBHOOK_HOST = os.environ.get("BOT_HOST")
sql_config = {
    "host": 'localhost',
    "user": os.environ.get("SQL_USER"),
    "password": os.environ.get("SQL_PASS"),
    "db": os.environ.get("SQL_DB"),
    "charset": 'utf8'
}

PORT = os.environ.get("BOT_PORT")

review_channel = -1001443580761

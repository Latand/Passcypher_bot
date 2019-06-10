import random

CONFIG_PREPARE = """
import os

TOKEN = "{bot_token}"

sql_config = {{
    "host": 'localhost',
    "user": "{sql_user}",
    "password": "{sql_pass}",
    "db": "{db_name}",
    "charset": 'utf8mb4'
}}

Reviews_state = False
# Set Reviews_state = True for enabling opportunity to leave reviews (probably not needed)
review_channel = -111
admin_id = {admin_id}

Webhook_state = False

# Set Webhook_state = True for enabling Webhook.
WEBHOOK_PATH = f'/{{TOKEN}}'
WEBHOOK_HOST = os.environ.get("BOT_HOST")
WEBHOOK_URL = f"https://{{WEBHOOK_HOST}}{{WEBHOOK_PATH}}/"
WEBAPP_PORT = os.environ.get("BOT_PORT")
WEBAPP_HOST = '127.0.0.1'
"""

secret_file = """
def key_func(__):
    return {digit}


def key_func_back(master, code):
    code = int(code)
    return str(code // {digit})
"""


def setup_secret():
    with open("secret.py", "w") as f:
        f.write(secret_file.format(digit=random.randint(2, 20)))
    print("Secret file is written successfully\n")


def setup_sql():
    print("Starting to create tables")
    from sql import sql

    sql.execute("""
    CREATE TABLE `users` (
      `chat_id` int(11) NOT NULL,
      `language` varchar(6) NOT NULL,
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `google` varchar(1000) DEFAULT NULL,
      `enabled` tinyint(4) NOT NULL DEFAULT '0',
      `blocked` tinyint(4) NOT NULL DEFAULT '0'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    sql.execute("""
    ALTER TABLE `users`
      ADD PRIMARY KEY (`id`,`chat_id`);""")

    print("Database created\n")


def setup_config():
    bot_token = input("Enter Bot token from Botfather\n")
    sql_user = input("Enter name of the sql user\n")
    sql_pass = input("Enter the password for sql db\n")
    db_name = input("Enter the db name\n")
    admin_id = input("Enter your chat_id from @ShowJsonBot\n")
    config = CONFIG_PREPARE.format(bot_token=bot_token,
                                   sql_user=sql_user,
                                   sql_pass=sql_pass,
                                   db_name=db_name,
                                   admin_id=admin_id)

    with open("config.py", "w") as f:
        f.write(config)
    print("Config is written successfully\n")


# Set up secret file
setup_secret()

choice = input("Do you want fill the config now? Enter y/n\n"
               "Enter N/n if you have filled the config manually (Do it first, if you haven't)\n")

if choice.lower() == "y":
    choice = input("Have you set up MYSQL? y/n\n")
    if choice.lower() == "y":
        # set up config
        setup_config()
        try:
            setup_sql()
        except Exception as err:
            print(f"Error {err} occurred! Are you sure you have MYSQL set up and you filled the config \
with the valid data?")
    else:
        print("Sorry, set it up first")
else:
    choice = input("Have you set up MYSQL? y/n\n")
    if choice.lower() == "y":
        try:
            setup_sql()
        except Exception as err:
            print(
                f"Error {err} occurred! Are you sure you have MYSQL set up, the config is filled with the valid data?")
    else:
        print("Sorry, set it up first")
    print("Bye")

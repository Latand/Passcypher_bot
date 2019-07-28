import os
import secrets
from pathlib import Path

TOKEN = os.environ.get("BOT_TOKEN_CYPHER")
sql_config = {
    "host": "127.0.0.1",
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "db": "main",
    "charset": 'utf8mb4'
}
I18N_DOMAIN = 'pcypher'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

Reviews_state = False
# Set Reviews_state = True for enabling opportunity to leave reviews (probably not needed)
review_channel = -1001443580761
admin_id = 362089194

Webhook_state = False

# Set Webhook_state = True for enabling Webhook.
WEBHOOK_PATH = f'/{secrets.token_urlsafe(128)}'
WEBHOOK_HOST = os.environ.get("BOT_HOST")
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}/"
WEBAPP_PORT = os.environ.get("BOT_PORT")
WEBAPP_HOST = '127.0.0.1'

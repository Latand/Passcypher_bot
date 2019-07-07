from functools import lru_cache

texts = {
    "en": {
        "changed": """Language has changed to 🇬🇧<b>EN</b>

<b>{users}</b> users are using this bot. 

<b>{passwords}</b> passwords encrypted.
<b>{messages}</b> messages received.

Start using this bot: /info""",
        "stats": """
<b>{users}</b> users are using this bot. 

<b>{passwords}</b> passwords encrypted.
<b>{messages}</b> messages received.
        """,
        "describe en 1": """
<b>How to use this bot:</b>

☑️1. Use command /encode to start encrypting your password.
You will be asked to enter your <code>MASTER PASSWORD</code>.
Master password will be needed to <b>decode</b> the encoded password afterwards.
<b> THE BOT DELETES YOUR MESSAGES WITH PASSWORDS AFTER 10 SECONDS</b>
📋<i>Example:</i> my-master-password-123
""",
        "describe en 2": """
☑️2. You will be asked to enter your password/phrase which you want to encode.
Your password/phrase can be no more than 400 characters long and contain only characters from this list:
<pre>{allowed_chars} </pre>
<b> THE BOT DELETES YOUR MESSAGES WITH PASSWORDS AFTER 10 SECONDS</b>

📋<i>Example:</i> password1993
""",
        "describe en 3": """
☑️3. You will receive the encoded password and the code, which will be needed to decode.

📋<i>Example:</i>


#encoded_pass: '<code>pЗ]/"aAЪ"PRsJ*sг6wю2ozr0P£Jd Ю/1 3ЛYJ9 - эu98&)/3s^т__хь</code>'

Key:

#key: '<code>421470377929804</code>'

""",
        "describe en 4": """
☑️4. Store this info wherever you want. Return to the bot whenever you want to decode it.
<b> THE BOT DELETES YOUR MESSAGES WITH PASSWORDS AFTER 10 SECONDS</b>

⚠️<b>THE BOT DOES NOT STORE THE PASSWORDS, JUST THE LANGUAGE INFO</b>

Start: /encode
""",

        "describe de 1": """
<b>How to use this bot:</b>

Decoding:

☑️1. Forward message with your encoded password and key you received from the bot previously.

""",
        "describe de 2": """
☑️2. You will be asked to enter your <code>Master password</code>.

<b> THE BOT DELETES YOUR MESSAGES WITH PASSWORDS AFTER 10 SECONDS</b>

📋<i>Example:</i> my-master-password-123
""",
        "describe de 3": """
☑️3. You will receive your password inside citation marks.

⚠️<b>THE BOT DOES NOT STORE THE PASSWORDS, JUST THE LANGUAGE INFO</b>

⚠️<b>WE CHANGE THE TOKEN FROM THE BOT EVERY MONTH SO ALL PREVIOUS MESSAGES CAN NOT BE ACCESSED</b>

Start: /encode
""",
        "encode master": """
Please enter your master password.
You can make everything faster with Google Authenticator! 
Press /g_auth_info

""",
        "g_auth info": """To encrypt your phrase/file you need to enter a master password each time you want to encrypt or decrypt, or\
 you can enable <b>Google Authenticator</b> and enter one-time codes from your phone <b>only to decrypt</b>\
  your passwords. \
(Master password will be kept in database then) 

Please make your choice (you can change it later with command /reset_google_auth
        """,

        "enable_g_auth": "Setup",
        "g_auth decode": "Enter the code from the app",
        "google_auth setup 1": """
Please ensure you have the app installed.
<a href= "https://itunes.apple.com/gb/app/google-authenticator/id388497605?mt=8">IOS</a>
<a href= "https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_GB">Android</a>

Press continue when you done. After you receive the code - write it down somewhere.
""",
        "continue": "Continue",
        "google_auth setup 2": """
You will receive a recovery code and a link below.
<b>IT WILL BE AUTOMATICALLY DELETED AFTER YOU CONFIRM</b>
""",
        "google_auth setup 3": "Please enter the code from the Google Authenticator\n"
                               "Pay attention that it updates every 30 sec.",
        "confirm yes": "Confirmation successful, you can proceed. /encode",
        "confirm no": "Confirmation unsuccessful, please try again",
        "invalid code": "Code is incorrect, try again or /cancel",
        "already enabled": "You have already received the Google Authenticator code",

        "reset gauth": "Here you can enable and disable your Google Authenticator settings",
        "turn on": "Turn on",
        "turn off": "Turn off",
        "not set": "Google Authenticator is not set for you. Press /g_auth_info",
        "done": "That is done",

        "password": """Enter phrase you want to encrypt.
It should be under 400 characters, for best results there should be only characters from this list:
<pre>{allowed_chars} </pre>
<b> THE BOT DELETES YOUR MESSAGES WITH PASSWORDS AFTER 10 SECONDS</b>
""",
        "result_encode":
            """<code>----------------------------
ENCRYPTION STARTS HERE
----------------------------
{passw}
----------------------------
ENCRYPTION ENDS HERE
----------------------------
CODE
{code}
----------------------------
</code>

Hint: {hint}
Save this message wherever you want and forward it to the bot should you need to decode it.
    """,
        "result_encode_doc":
            """
----------------------------
ENCRYPTION STARTS HERE
----------------------------
{passw}
----------------------------
ENCRYPTION ENDS HERE
----------------------------
CODE
{code}
----------------------------
Hint: {hint}
    """,
        "entered_master": """Enter your encrypted password.
<b> THE BOT DELETES YOUR MESSAGES WITH PASSWORDS AFTER 10 SECONDS</b>

""",
        "enter_code": """
Enter key for decode (digits only)""",
        "decoded_result": """
Your decoded password is inside citation marks '<code>{password}</code>'
""",
        "next": "Next page",
        "prev": "Previous page",

        "OOPS": """
Looks like the input is invalid...
To decode your password - forward the message with encoded password you received from bot.
<a href= 'https://telegra.ph/file/a9f99684284a92eb2a6a0.png'>ᅠ</a>
Perhaps you wanted to encrypt this message? Click <b> Encrypt </b>.""",
        "large": "Error has occurred... Too long phrase. Try to enter a phrase under 400 characters.",
        "bad_char": "You have restricted character in phrase.\n"
                    "Please try again.",
        "g_auth": "Use Google auth",
        "no_g_auth": "Use Master password",
        "advice": """Please, it is important for me to receive a response and advice from you.
How would you change the bot? Any comments are appreciated. 

Your comment will be posted <b>anonymously</b> in our channel @pcypher
Or you can just rate the bot using this link: https://t.me/pcypher/16
""",

        "g_advice": "Give an advice to the bot",

        "adv_message": """
Your advice: 

{advice}

Write your advice in the next message.
""",
        "send_adv": "Publish",
        "cancel": "Cancel",
        "cancelled": "Cancelled",
        "post_advice": """
#Reviews Post:

<b>{}</b>
""",

        "ENCODE": "🔒 Encode",
        "DECODE": "🔑 Decode",
        "INFO": "ℹ️How to use",
        "LANGUAGE": "🇬🇧 Set language",
        "GOOGLE_AUTH": "🔐 Two step verification",
        "REVIEWS": "📝 Write a review",

        "gauth_error": "An error has occurred, you lost the Google authenticator settings\n"
                       "Please re-configure it once again /g_auth_info",
        "error_g_state": "Please press on button to continue or /cancel",
    },
    "ua": {
        "changed": ("Мова була змінена на <b>UA</b>\n"
                    "\n"
                    "<b>{users}</b> Користувачів використовують цього бота.\n"
                    "<b>{passwords}</b> паролів зашифровано.\n"
                    "<b>{messages}</b> повідомлень оброблено.\n"
                    "\n"
                    "Почните користуватися ботом: /info\n"
                    " "),

        "stats": ("\n"
                  "<b>{users}</b> Користувачів використовують цього бота.\n"
                  "<b>{passwords}</b> паролів зашифровано.\n"
                  "<b>{messages}</b> повідомлень оброблено.\n"
                  "        "),
        "describe en 1": """
<b>Як використовувати цього бота:</b> 

Шифрування:

☑️1. Використайте комманду /encode, задля того щоб почати шифрування пароля.
Вас попросять ввести ваш  <code>МАСТЕР ПАРОЛЬ</code>.
Мастер пароль знадобиться, задля того щоб пізніше <b>розшифрувати</b> зашифровані паролі.
<b> БОТ ВИДАЛЯЄ повідомлення з паролем ЧЕРЕЗ 10 СЕКУНД </b>

📋<i>Приклад:</i> my-master-password-123
""",
        "describe en 2": """
☑️2. Вас попросять ввести пароль/фразу, котру ви бажаєте зашифрувати.
Пароль/фраза може бути довжиною до 400 символів та може містити тільки символи з цього списку:
<pre>{allowed_chars} </pre>

<b> БОТ ВИДАЛЯЄ повідомлення з паролем ЧЕРЕЗ 10 СЕКУНД </b>

📋<i>Приклад:</i> password1993
""",
        "describe en 3": """
☑️3. Ви отримаєте пароль в зашифрованому вигляді та код, котрий знадобиться пізніше, щоб розшифрувати.

📋<i>Приклад:</i>

Зашифрований пароль:

#encoded_pass: '<code>pЗ]/"aAЪ"PRsJ*sг6wю2ozr0P£Jd Ю/1 3ЛYJ9 - эu98&)/3s^т__хь</code>

Код:
#key: '<code>421470377929804</code>'

""",
        "describe en 4": """
☑️4. Збережіть цю інформацію де вам зручно, та звертайтесь до бота, коли вам знодиться розшифрувати пароль. 

⚠️<b>БОТ НЕ ЗБЕРІГАЄ ВАШІ ПАРОЛІ, ЗБЕРІГАЄТЬСЯ ТІЛЬКІ ОБРАНА МОВА</b>

Почати: /encode
""",

        "describe de 1": """
<b>Як використовувати цього бота:</b>

Розшифрування:

☑️1. Перешліть боту повідомлення з зашифрованим паролем та кодом, котрі ви отримали від бота.

""",
        "describe de 2": """
☑️2. Вас попрохають ввести ваш  <code>МАСТЕР ПАРОЛЬ</code>.
Мастер пароль знадобиться, задля того щоб пізніше <b>розшифрувати</b> зашифровані паролі.
<b> БОТ ВИДАЛЯЄ повідомлення з паролем ЧЕРЕЗ 10 СЕКУНД </b>

📋<i>Приклад:</i> my-master-password-123
""",
        "describe de 3": """
☑️3. На виході ви отримуєте свій пароль всередені лапок.

⚠️<b>БОТ НЕ ЗБЕРІГАЄ ВАШІ ПАРОЛІ, ЗБЕРІГАЄТЬСЯ ТІЛЬКІ ОБРАНА МОВА</b>

Почати: /encode
""",
        "encode master": ("Введіть свій мастер пароль, котрий вы гарно пам`ятаєте.\n"
                          "<b> БОТ ВИДАЛЯЄ повідомлення з паролем ЧЕРЕЗ 10 СЕКУНД </b>\n"
                          "\n"
                          "Пришвидшіть процес за допомогою Google Authenticator! \n"
                          "\n"
                          "Натисніть для подальшої інформації /g_auth_info\n"
                          "\n"),

        "g_auth info": ("Щоб зашифрувати файл/пароль ви повинні вводити мастер пароль кожного разу, щоб зашифрувати\\n"
                        " або розшифрувати. \n"
                        "Але ви можете увімкнути Google Authenticator та вводити одноразові паролі зі свого телефону \\n"
                        "<b>тільки для розшифровки</b> своїх паролей (Але тоді мастер пароль буде зберігатися в нашій базі даних\n"
                        "\n"
                        "Зробіть свій вибір (ви маєте змогу пізніше відключити цю функцію за допомогою команди /reset_google_auth )\n"
                        "        "),
        "enable_g_auth": "Почати налаштування",
        "g_auth decode": "Введіть код з додатку",
        "google_auth setup 1": ("\n"
                                "Зпочатку переконайтесь, що в вас встановлений додаток.\n"
                                "<a href= \"https://itunes.apple.com/gb/app/google-authenticator/id388497605?mt=8\">IOS</a>\n"
                                "<a href= \"https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_GB\">Android</a>\n"
                                "\n"
                                "Натисніть продовжити коли закінчите, після того як отрумаєте код - запишіть його де-небудь."),
        "continue": "Продовжити",
        "google_auth setup 2": ("\n"
                                "Ви отримуєте код для відновлення нижче .\n"
                                "<b>ПОВІДОМЛЕННЯ БУДЕ ВИДАЛЕНЕ ПІСЛЯ ПІДТВЕРДЖЕННЯ</b>\n"),
        "google_auth setup 3": "Будьласка введить код котрий ви отримали в Google Authenticator\n"
                               "Зверніть увагу, що код оновлюється кожні 30 сек",
        "confirm yes": "Успішно підтверджено, продовжуйте. /encode",
        "confirm no": "Код не був підтверджений, спробуйте ще раз",
        "invalid code": "Хибний код, спробуйте знов або скасуйте /cancel",

        "already enabled": "Ви вже налаштовували Google Authenticator",

        "reset gauth": "Тут ви маєте змогу увімкнути та вимкнути налаштування Google Authenticator",
        "turn on": "Увімкнути",
        "turn off": "Вимкнути",
        "not set": "Ви ще не налаштовували Google Authenticator. Натисніть /g_auth_info",
        "done": "Готово",

        "password": ("Введіть пароль, котрий бажаєте зашифрувати.\n"
                     "Він повинен бути довжиною до 400 символів та рекомендується задля кращого результату використовувати символи тільки з цього списку:\n"
                     "<b> БОТ ВИДАЛЯЄ повідомлення з паролем ЧЕРЕЗ 10 СЕКУНД </b>\n"
                     "\n"
                     "<pre>{allowed_chars} </pre>\n"),
        "result_encode":
            ("<code>----------------------------\n"
             "ENCRYPTION STARTS HERE\n"
             "----------------------------\n"
             "{passw}\n"
             "----------------------------\n"
             "ENCRYPTION ENDS HERE\n"
             "----------------------------\n"
             "CODE\n"
             "{code}\n"
             "----------------------------\n"
             "</code>\n"
             "Підказка: {hint}   \n"
             "         \n"
             "Збережіть цю інформацію де вам зручно, та звертайтесь до бота, коли вам знодиться розшифрувати пароль. \n"),
        "result_encode_doc":
            """
----------------------------
ENCRYPTION STARTS HERE
----------------------------
{passw}
----------------------------
ENCRYPTION ENDS HERE
----------------------------
CODE
{code}
----------------------------
    
Підказка: {hint}
    """,
        "entered_master": """Введіть зашифрований пароль.
<b> БОТ ВИДАЛЯЄ повідомлення з паролем ЧЕРЕЗ 10 СЕКУНД </b>

""",
        "enter_code": """
Введіть ключ для розшифрування (тільки цифри)""",
        "decoded_result": ("\n"
                           "Ваш розшифрований пароль знаходиться всередені лапок \n"
                           "'<code>{password}</code>'\n"
                           "\n"),
        "next": "Далі",
        "prev": "Назад",

        "OOPS": ("\n"
                 "Схоже, що ви ввели хибний запит...\n"
                 "Задля того, щоб розкодувати - перешліть повідомлення, котре ви отримали від бота с закодованим паролем. \n"
                 "<a href= 'https://telegra.ph/file/a9f99684284a92eb2a6a0.png'>ᅠ</a>\n"
                 "Можливо ви хотіли зашифрувати це повідомлення? Натисніть <b> зашифрувати </b>."),
        "large": "Виникла помилочка... Занадто довгий пароль. Будьласка введіть пароль довжиною до 400 символів.",
        "bad_char": "У вас у паролі є неприпустимий символ\n"
                    "Будьласка спробуйте ще раз.",

        "g_auth": "Використовувати Google authenticator",
        "no_g_auth": "Використовувати Мастер password",

        "advice": (
            "Для мене дуже важливо ваша думка та будь-який відгук про бота. Що ви б покращили або змінили? Будь-яка допомога буде цінитись. \n"
            "\n"
            "Ваш коментарій буде опублікований на нашому каналі @pcypher абсолютно анонімно.\n"
            "Або ви можете поставити оцінку боту за цим посиланням: https://t.me/pcypher/16\n"),
        "g_advice": "Надати пораду ботові",
        "adv_message": ("\n"
                        "Ваша порада: \n"
                        "\n"
                        "{advice}\n"
                        "\n"
                        "Напишіть вашу пораду ботові у наступному повідомленні.\n"),
        "send_adv": "Опубліковати відгук",
        "cancel": "Скасувати",
        "cancelled": "Скасовано",
        "post_advice": """
#Reviews Post:

<b>{}</b>
""",

        "ENCODE": "🔒 Зашифрувати",
        "DECODE": "🔑 Розшифрувати",
        "INFO": "ℹ️Як використовувати",
        "LANGUAGE": "🇺🇦 Змінити мову",
        "GOOGLE_AUTH": "🔐 Двохетапна верифікація",
        "REVIEWS": "📝 Залишити відгук",
        "gauth_error": "Сталася помилка, у вас збилася настройка Google authenticator. \n"
                       "Будь ласка, налаштуйте його заново. /g_auth_info",
        "error_g_state": "Будь ласка, натисніть продовжити для того, щоб налаштувати, або натисніть для \
скасування /cancel"
    }
}


class Other_Texts(object):

    def __init__(self):
        pass

    WELCOME_MESSAGE = """
Hello, <b>{}</b>
This bot is designed to encrypt your passwords so you can store them publicly, for example in your \
<code>Telegram saved messages.</code>

Firstly, let's choose your language
"""
    SET_LANGUAGE_MESSAGE = """
Hello, <b>{}</b>
Firstly, let's choose your language
"""
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


allowed_chars = 'qwertyuiopasdfghjklzxcvbnm,.!£$%^&*()[];_-+1234567890йцукенгшщзхъфывапролджэячсмитьбю'
to_mix = 'qwertyuiop asdfghjklzxcvbnm,.!£$%^&*()[];_-+1234567890 йцукенгшщзхъфывапролджэячсмитьбю'


class Links:
    INSTRUCTION = "https://telegra.ph/How-to-Use-Passcypher-Instruction-EN-06-02"
    def __init__(self, lang):
        self.INSTRUCTION = {
            "en": "https://telegra.ph/How-to-Use-Passcypher-Instruction-EN-06-02",
            "ru": "https://telegra.ph/Kak-ispolzovat-Passcypher-Instrukciya-06-03",
            "ua": "https://telegra.ph/Kak-ispolzovat-Passcypher-Instrukciya-06-03",
        }[lang]

        self.ENCRYPT = {
            "en": "https://telegra.ph/Passwords-Encryption-Process-06-02",
            "ru": "https://telegra.ph/Process-zashirofki-parolej-06-03",
            "ua": "https://telegra.ph/Process-zashirofki-parolej-06-03",
        }[lang]

        self.DECRYPT = {
            "en": "https://telegra.ph/Passwords-Decryption-Process-06-02",
            "ru": "https://telegra.ph/Process-deshifrovki-parolej-06-09",
            "ua": "https://telegra.ph/Process-deshifrovki-parolej-06-09",
        }[lang]

        self.GOOGLE_AUTH = {
            "en": "https://telegra.ph/Passcypher-Google-Authenticator-06-02",
            "ru": "https://telegra.ph/Passcypher-Ispolzovanie-Google-Authenticator-06-07",
            "ua": "https://telegra.ph/Passcypher-Ispolzovanie-Google-Authenticator-06-07",
        }[lang]


@lru_cache()
def links(lang) -> Links:
    return Links(lang)


def get_text(language, key):
    return texts[language][key]

#
#     "ru": {
#         "changed": ("Язык был изменен на 🇷🇺<b>RU</b>\n"
#                     "\n"
#                     "<b>{users}</b> Пользователей используют этого бота.\n"
#                     "<b>{passwords}</b> паролей зашифровано.\n"
#                     "<b>{messages}</b> сообщений обработано.\n"
#                     "\n"
#                     "Начните использовать этого бота: /info\n"
#                     " "),
#
#         "stats": ("\n"
#                   "<b>{users}</b> Пользователей используют этого бота.\n"
#                   "<b>{passwords}</b> паролей зашифровано.\n"
#                   "<b>{messages}</b> сообщений обработано.\n"
#                   "        "),
#         "describe en 1": """
# <b>Как использовать этого бота:</b>
#
# Зашифровка:
#
# ☑️1. Используйте комманду /encode, чтобы начать шифрование пароля.
# Вас попросят ввести ваш  <code>МАСТЕР ПАРОЛЬ</code>.
# Мастер пароль понадобится, чтобы позже <b>расшифровать</b> зашифрованные пароли.
#
# 📋<i>Пример:</i> my-master-password-123
# """,
#         "describe en 2": """
# ☑️2. Вас попросят ввести пароль/фразу, который вы хотите зашифровать.
# Пароль/фраза может быть длиной до 400 символов и может содержать только символы из этого списка:
# <pre>{allowed_chars} </pre>
#
# <b> БОТ УДАЛЯЕТ СООБЩЕНИЯ С ПАРОЛЯМИ ЧЕРЕЗ 10 СЕКУНД</b>
#
# 📋<i>Пример:</i> password1993
# """,
#         "describe en 3": """
# ☑️3. Вы получите пароль в зашифрованном виде и код, который понадобится позже, чтобы расшифровать.
#
# 📋<i>Пример:</i>
#
# Зашифрованный пароль:
#
# #encoded_pass: '<code>pЗ]/"aAЪ"PRsJ*sг6wю2ozr0P£Jd Ю/1 3ЛYJ9 - эu98&)/3s^т__хь</code>
#
# Код:
# #key: '<code>421470377929804</code>'
#
# """,
#         "describe en 4": """
# ☑️4. Сохраните эту инфромацию где захотите, и возвращайтесь в бота, когда вы захотите расшифровать пароль.
#
# ⚠️<b>БОТ НЕ СОХРАНЯЕТ ВАШИ ПАРОЛИ, СОХРАНЯЕТСЯ ТОЛЬКО ВЫБРАННЫЙ ЯЗЫК</b>
#
# Начать: /encode
# """,
#
#         "describe de 1": """
# <b>Как использовать этого бота:</b>
#
# Расшифровка:
#
# ☑️1. Перешлите боту сообщение с защифрованным паролем и кодом, которое вы получили от бота.
#
# """,
#         "describe de 2": """
# ☑️2.Вас попросят ввести ваш  <code>МАСТЕР ПАРОЛЬ</code>.
# Мастер пароль понадобится, чтобы позже <b>расшифровать</b> зашифрованные пароли.
# <b> БОТ УДАЛЯЕТ СООБЩЕНИЯ С ПАРОЛЯМИ ЧЕРЕЗ 10 СЕКУНД</b>
#
# 📋<i>Пример:</i> my-master-password-123
# """,
#         "describe de 3": """
# ☑️3. На выходе вы получите свой пароль внутри кавычек.
#
# ⚠️<b>БОТ НЕ СОХРАНЯЕТ ВАШИ ПАРОЛИ, СОХРАНЯЕТСЯ ТОЛЬКО ВЫБРАННЫЙ ЯЗЫК</b>
#
# Начать: /encode
# """,
        # "encode master": ("Введите свой мастер пароль, который вы хорошо помните.\n"
        #                   "<b> БОТ УДАЛЯЕТ СООБЩЕНИЯ С ПАРОЛЯМИ ЧЕРЕЗ 10 СЕКУНД</b>\n"
        #                   "\n"
        #                   "Ускорьте процесс с помощью Google Authenticator!\n"
        #                   "\n"
        #                   "Нажми для подробной информации /g_auth_info\n"
        #                   "\n")
    # ,
#
#         "g_auth info": ("Чтобы зашифровать файл/пароль вы должны вводить мастер пароль каждый раз, чтобы зашифровать\\n"
#                         " или расшифровать. \n"
#                         "Но вы можете включить Google Authenticator и вводить одноразовые пароли со своего телефона \\n"
#                         "<b>только для расшифровки</b> своих паролей (Но тогда мастер пароль будет храниться в нашей базе данных\n"
#                         "\n"
#                         "Сделайте свой выбор (вы сможете позже отключать эту функцию с помощью команды /reset_google_auth )\n"
#                         "        "),
#         "enable_g_auth": "Начать настройку",
#         "g_auth decode": "Введите код из приложения",
#         "google_auth setup 1": ("\n"
#                                 "Для начала убедитесь, что у вас установлено приложение.\n"
#                                 "<a href= \"https://itunes.apple.com/gb/app/google-authenticator/id388497605?mt=8\">IOS</a>\n"
#                                 "<a href= \"https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_GB\">Android</a>\n"
#                                 "\n"
#                                 "Нажмите продолжить когда закончите, после того как получите код - запишите его где нибудь."),
#         "continue": "Продолжить",
#         "google_auth setup 2": ("\n"
#                                 "Вы получите код для восстановления ниже .\n"
#                                 "<b>СООБЩЕНИЕ БУДЕТ УДАЛЕНО ПОСЛЕ ПОДТВЕРЖДЕНИЯ</b>\n"),
#         "google_auth setup 3": "Пожалуйста введите код который вы получили в Google Authenticator\n"
#                                "Обратите внимание, что код обновляется каждые 30 сек",
#         "confirm yes": "Успешно подтверждено, можете продолжать. /encode",
#         "confirm no": "Код не был подтвержден, попробуйте снова",
#         "invalid code": "Код неверный, попробуйте снова или отмените /cancel",
#
#         "already enabled": "Вы уже настраивали Google Authenticator",
#
#         "reset gauth": "Тут вы можете включать и выключать настройки Google Authenticator",
#         "turn on": "Включить",
#         "turn off": "Выключить",
#         "not set": "Вы еще не настраивали Google Authenticator. Нажмите /g_auth_info",
#         "done": "Готово",
#
        # "password": ("Введите пароль, который хотите зашифровать.\n"
        #              "Он должен быть длиной до 400 символов и рекомендуется для лучшего результата использовать символы только из этого списка:\n"
        #              "<pre>{allowed_chars} </pre>\n")
# ,
#         "result_encode":
#             """<code>----------------------------
# ENCRYPTION STARTS HERE
# ----------------------------
# {passw}
# ----------------------------
# ENCRYPTION ENDS HERE
# ----------------------------
# CODE
# {code}
# ----------------------------
# </code>
# Сохраните это сообщение где угодно и перешлите боту когда захотите расшифровать свой пароль.
#
# Подсказка: {hint}
#     """,
#         "result_encode_doc":
#             """
# ----------------------------
# ENCRYPTION STARTS HERE
# ----------------------------
# {passw}
# ----------------------------
# ENCRYPTION ENDS HERE
# ----------------------------
# CODE
# {code}
# ----------------------------
#
# Подсказка: {hint}
#     """,
#         "entered_master": """Введите ваш зашифрованный пароль.
# <b> БОТ УДАЛЯЕТ СООБЩЕНИЯ С ПАРОЛЯМИ ЧЕРЕЗ 10 СЕКУНД</b>
# """,
#         "enter_code": """
# Введите ключ для расшифровывания (только цифры)""",
#         "decoded_result": """
# Ваш расшифрованный пароль находится внутри кавычек
# '<code>{password}</code>'
#
#
# """,
#         "next": "Дальше",
#         "prev": "Назад",
#
#         "OOPS": ("\n"
#                  "Похоже, что вы ввели неверный запрос...\n"
#                  "\n"
#                  "Для того, чтобы раскодировать - пришлите сообщение, которое вы получили от бота с закодированным паролем. \n"
#                  "<a href= 'https://telegra.ph/file/a9f99684284a92eb2a6a0.png'>ᅠ</a>\n"
#                  "\n"
#                  "Возможно вы хотели зашифровать это сообщение? Нажмите <b>зашифровать</b>."),
#         "large": "Ошибочка произошла... Слишком длинный пароль. постарайтесь ввести пароль длиной до 400 символов.",
#         "bad_char": "У вас в пароле есть недопустимый символ\n"
#                     "Пожалуйста попробуйте еще раз.",
#
#         "g_auth": "Использовать Google authenticator",
#         "no_g_auth": "Использовать Мастер password",
#
#         "advice": ("Для меня очень важно ваше мнение и любой отзыв о боте. \n"
#                    "Что бы вы сделали лучше, что бы вы изменили? Любая помощь оценится. \n"
#                    "\n"
#                    "Ваш комментарий будет опубликован в нашем канале @pcypher абсолютно анонимно.\n"
#                    "\n"
#                    "Или вы можете поставить оценку боту по этой ссылке: https://t.me/pcypher/16"),
#         "g_advice": "Дать совет боту",
#         "adv_message": ("\n"
#                         "Ваш совет: \n"
#                         "\n"
#                         "{advice}\n"
#                         "\n"
#                         "Напишите ваш совет боту в следующем сообщении.\n"),
#         "send_adv": "Опубликовать отзыв",
#         "cancel": "Отмена",
#         "cancelled": "Отменено",
#         "post_advice": ("\n"
#                         "#Reviews Post:\n"
#                         "\n"
#                         "<b>{}</b>\n"),
#
#         "ENCODE": "🔒 Зашифровать",
#         "DECODE": "🔑 Расшифровать",
#         "INFO": "ℹ️Как использовать",
#         "LANGUAGE": "🇷🇺 Сменить язык",
#         "GOOGLE_AUTH": "🔐 Двухэтапная верификация",
#         "REVIEWS": "📝 Оставить отзыв",
#         "gauth_error": "Произошла ошибка, у вас сбилась настройка Google authenticator\n"
#                        "Пожалуйста, настройте его заново /g_auth_info",
#         "error_g_state": "Пожалуйста, нажмите продолжить для того, чтобы настроить, или нажмите отмена /cancel"
#     },

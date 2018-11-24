texts = {
    "en": {
        "changed": "Language has changed to 🇬🇧<b>EN</b>",
        "describe en 1": """
<b>How to use this bot:</b>

☑️1. Use command /encode to start encrypting your password.
You will be asked to enter your <code>MASTER PASSWORD</code>.
Master password will be needed to <b>decode</b> the encoded password afterwards.
⚠️<b>YOU MUST DELETE THE MESSAGE WITH YOUR PASSWORD AFTERWARDS</b>

📋<i>Example:</i> my-master-password-123
""",
        "describe en 2": """
☑️2. You will be asked to enter your password/phrase which you want to encode.
Your password/phrase can be no more than 400 characters long and contain only characters from this list:
<pre>{allowed_chars} </pre>
⚠️<b>YOU MUST DELETE THE MESSAGE WITH YOUR PASSWORD AFTERWARDS</b>

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

⚠️<b>YOU MUST DELETE THE MESSAGES WITH YOUR PASSWORD FROM THE BOT</b>

⚠️<b>THE BOT DOES NOT STORE THE PASSWORDS, JUST THE LANGUAGE INFO</b>

⚠️<b>WE CHANGE THE TOKEN FROM THE BOT EVERY MONTH SO ALL PREVIOUS MESSAGES CAN NOT BE ACCESSED</b>

Start: /encode
""",

        "describe de 1": """
<b>How to use this bot:</b>

Decoding:

☑️1. Forward message with your encoded password and key you received from the bot previously.

""",
        "describe de 2": """
☑️2. You will be asked to enter your <code>Master password</code>.

⚠️<b>YOU MUST DELETE THE MESSAGE WITH YOUR PASSWORD AFTERWARDS</b>

📋<i>Example:</i> my-master-password-123
""",
        "describe de 3": """
☑️3. You will receive your password inside citation marks.

⚠️<b>YOU MUST DELETE THE MESSAGES WITH YOUR PASSWORD FROM THE BOT</b>

⚠️<b>THE BOT DOES NOT STORE THE PASSWORDS, JUST THE LANGUAGE INFO</b>

⚠️<b>WE CHANGE THE TOKEN FROM THE BOT EVERY MONTH SO ALL PREVIOUS MESSAGES CAN NOT BE ACCESSED</b>

Start: /encode
""",
        "encode master": """
Please enter your master password.
You can make everything faster with Google Authenticator! 
Press /g_auth_info

⚠️<b>YOU MUST DELETE THE MESSAGES WITH YOUR PASSWORD FROM THE BOT</b>
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

⚠️<b>YOU MUST DELETE THE MESSAGES WITH YOUR PASSWORD FROM THE BOT</b>
""",
        "result_encode":
        """
Encoded (inside citation marks):

#encoded_pass: '<code>{passw}</code>'

Key:

#key: '<code>{code}</code>'

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
To encode your password press /encode

To decode your password - forward the message with encoded password you received from bot.
It should look like that:

#encoded_pass: '<code>password</code>'

#key: '<code>123456</code>'


<a href= 'https://telegra.ph/file/a9f99684284a92eb2a6a0.png'>ᅠ</a>""",
        "large": "Error has occurred... Too long phrase. Try to enter a phrase under 400 characters.",
        "bad_char": "You have restricted character in phrase.\n"
                    "Please try again.",
        "g_auth": "Use Google auth",
        "no_g_auth": "Use Master password"

    },
    "ru": {
        "changed": "Язык был изменен на 🇷🇺<b>RU</b>",
        "describe en 1": """
<b>Как использовать этого бота:</b> 

Зашифровка:

☑️1. Используйте комманду /encode, чтобы начать шифрование пароля.
Вас попросят ввести ваш  <code>МАСТЕР ПАРОЛЬ</code>.
Мастер пароль понадобится, чтобы позже <b>расшифровать</b> зашифрованные пароли.

⚠️<b>ВЫ ДОЛЖНЫ УДАЛИТЬ СООБЩЕНИЕ С ПАРОЛЕМ ИЗ ПЕРЕПИСКИ</b>

📋<i>Пример:</i> my-master-password-123
""",
        "describe en 2": """
☑️2. Вас попросят ввести пароль/фразу, который вы хотите зашифровать.
Пароль/фраза может быть длиной до 400 символов и может содержать только символы из этого списка:
<pre>{allowed_chars} </pre>


⚠️<b>ВЫ ДОЛЖНЫ УДАЛИТЬ СООБЩЕНИЕ С ПАРОЛЕМ ИЗ ПЕРЕПИСКИ</b>

📋<i>Пример:</i> password1993
""",
        "describe en 3": """
☑️3. Вы получите пароль в зашифрованном виде и код, который понадобится позже, чтобы расшифровать.

📋<i>Пример:</i>

Зашифрованный пароль:

#encoded_pass: '<code>pЗ]/"aAЪ"PRsJ*sг6wю2ozr0P£Jd Ю/1 3ЛYJ9 - эu98&)/3s^т__хь</code>

Код:
#key: '<code>421470377929804</code>'

""",
        "describe en 4": """
☑️4. Сохраните эту инфромацию где захотите, и возвращайтесь в бота, когда вы захотите расшифровать пароль.

⚠️<b>УДАЛЯЙТЕ ЛЮБЫЕ СООБЩЕНИЯ С ПАРОЛЯМИ В ПЕРЕПИСКЕ С БОТОМ</b>

⚠️<b>БОТ НЕ СОХРАНЯЕТ ВАШИ ПАРОЛИ, СОХРАНЯЕТСЯ ТОЛЬКО ВЫБРАННЫЙ ЯЗЫК</b>

⚠️<b>МЫ МЕНЯЕМ ТОКЕН БОТА КАЖДЫЙ МЕСЯЦ, ТАК ЧТО ДОСТУП К ПРОШЛЫМ СООБЩЕНИЯМ БУДЕТ УТЕРЯН</b>

Начать: /encode
""",

        "describe de 1": """
<b>Как использовать этого бота:</b>

Расшифровка:

☑️1. Перешлите боту сообщение с защифрованным паролем и кодом, которое вы получили от бота.

""",
        "describe de 2": """
☑️2.Вас попросят ввести ваш  <code>МАСТЕР ПАРОЛЬ</code>.
Мастер пароль понадобится, чтобы позже <b>расшифровать</b> зашифрованные пароли.

⚠️<b>ВЫ ДОЛЖНЫ УДАЛИТЬ СООБЩЕНИЕ С ПАРОЛЕМ ИЗ ПЕРЕПИСКИ</b>

📋<i>Пример:</i> my-master-password-123
""",
        "describe de 3": """
☑️3. На выходе вы получите свой пароль внутри кавычек.

⚠️<b>УДАЛЯЙТЕ ЛЮБЫЕ СООБЩЕНИЯ С ПАРОЛЯМИ В ПЕРЕПИСКЕ С БОТОМ</b>

⚠️<b>БОТ НЕ СОХРАНЯЕТ ВАШИ ПАРОЛИ, СОХРАНЯЕТСЯ ТОЛЬКО ВЫБРАННЫЙ ЯЗЫК</b>

⚠️<b>МЫ МЕНЯЕМ ТОКЕН БОТА КАЖДЫЙ МЕСЯЦ, ТАК ЧТО ДОСТУП К ПРОШЛЫМ СООБЩЕНИЯМ БУДЕТ УТЕРЯН</b>

Начать: /encode
""",
        "encode master": """Введите свой мастер пароль, который вы хорошо помните.
Ускорьте процесс с помощью Google Authenticator! 

Нажми для подробной информации /g_auth_info

⚠️<b>ВЫ ДОЛЖНЫ УДАЛИТЬ СООБЩЕНИЕ С ПАРОЛЕМ ИЗ ПЕРЕПИСКИ</b>
""",

        "g_auth info": """Чтобы зашифровать файл/пароль вы должны вводить мастер пароль каждый раз, чтобы зашифровать\
 или расшифровать. 
Но вы можете включить Google Authenticator и вводить одноразовые пароли со своего телефона \
<b>только дляр расшифровки</b> своих паролей (Но тогда мастер пароль будет храниться в нашей базе данных

Сделайте свой выбор (вы сможете позже отключать эту функцию с помощью команды /reset_google_auth )
        """,
        "enable_g_auth": "Начать настройку",
        "g_auth decode": "Введите код из приложения",
        "google_auth setup 1": """
Для начала убедитесь, что у вас установлено приложение.
<a href= "https://itunes.apple.com/gb/app/google-authenticator/id388497605?mt=8">IOS</a>
<a href= "https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_GB">Android</a>

Нажмите продолжить когда закончите, после того как получите код - запишите его где нибудь.""",
        "continue": "Продолжить",
        "google_auth setup 2": """
Вы получите код для восстановления ниже .
<b>СООБЩЕНИЕ БУДЕТ УДАЛЕНО ПОСЛЕ ПОДТВЕРЖДЕНИЯ</b>
""",
        "google_auth setup 3": "Пожалуйста введите код который вы получили в Google Authenticator\n"
                               "Обратите внимание, что код обновляется каждые 30 сек",
        "confirm yes": "Успешно подтверждено, можете продолжать. /encode",
        "confirm no": "Код не был подтвержден, попробуйте снова",
        "invalid code": "Код неверный, попробуйте снова или отмените /cancel",

        "already enabled": "Вы уже настраивали Google Authenticator",

        "reset gauth": "Тут вы можете включать и выключать настройки Google Authenticator",
        "turn on": "Включить",
        "turn off": "Выключить",
        "not set": "Вы еще не настраивали Google Authenticator. Нажмите /g_auth_info",
        "done": "Готово",

        "password": """Введите пароль, который хотите зашифровать.
Он должен быть длиной до 400 символов и рекомендуется для лучшего результата использовать символы только из этого списка:
<pre>{allowed_chars} </pre>
⚠️<b>ВЫ ДОЛЖНЫ УДАЛИТЬ СООБЩЕНИЕ С ПАРОЛЕМ ИЗ ПЕРЕПИСКИ</b>
""",
        "result_encode":
        """
Ваш зашифрованный пароль:
#encoded_pass: '<code>{passw}</code>'

Код:

#key: '<code>{code}</code>'


Сохраните это сообщение где угодно и перешлите боту когда захотите расшифровать свой пароль.

Подсказка: {hint}
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

Подсказка: {hint}
""",
        "entered_master": """Введите ваш зашифрованный пароль.
""",
        "enter_code": """
Введите ключ для расшифровывания (только цифры)""",
        "decoded_result": """
Ваш расшифрованный пароль находится внутри кавычек 
'<code>{password}</code>'

⚠️<b>ВЫ ДОЛЖНЫ УДАЛИТЬ СООБЩЕНИЕ С ПАРОЛЕМ ИЗ ПЕРЕПИСКИ</b>
""",
        "next": "Дальше",
        "prev": "Назад",

        "OOPS": """
Похоже, что вы ввели неверный запрос...
Для того, чтобы закодировать пароль нажмите /encode

Для того, чтобы раскодировать - пришлите сообщение, которое вы получили от бота с закодированным паролем. 
Оно должно быть в формате:


#encoded_pass: '<code>password</code>'

Код:

#key: '<code>123456</code>'


<a href= 'https://telegra.ph/file/a9f99684284a92eb2a6a0.png'>ᅠ</a>""",
        "large": "Ошибочка произошла... Слишком длинный пароль. постарайтесь ввести пароль длиной до 400 символов.",
        "bad_char": "У вас в пароле есть недопустимый символ\n"
                    "Пожалуйста попробуйте еще раз."

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
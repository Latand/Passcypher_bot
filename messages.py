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
        "encode": """Enter your master password you remember well.
⚠️<b>YOU MUST DELETE THE MESSAGES WITH YOUR PASSWORD FROM THE BOT</b>
""",
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
                    "Please try again."

    },
    "ru": {
        "changed": "Язык был изменен на 🇷🇺<b>RU</b>",
        "describe en 1": """
<b>Как искользовать этого бота:</b> 

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
<b>Как искользовать этого бота:</b>

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
        "encode": """Введите свой мастер пароль, который вы хорошо помните.
⚠️<b>ВЫ ДОЛЖНЫ УДАЛИТЬ СООБЩЕНИЕ С ПАРОЛЕМ ИЗ ПЕРЕПИСКИ</b>
""",
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
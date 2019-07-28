from functools import lru_cache


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
    def __init__(self, lang):
        self.INSTRUCTION = {
            "en": "https://telegra.ph/How-to-Use-Passcypher-Instruction-EN-06-02",
            "ru": "https://telegra.ph/Kak-ispolzovat-Passcypher-Instrukciya-06-03",
            "uk": "https://telegra.ph/Kak-ispolzovat-Passcypher-Instrukciya-06-03",
        }[lang]

        self.ENCRYPT = {
            "en": "https://telegra.ph/Passwords-Encryption-Process-06-02",
            "ru": "https://telegra.ph/Process-zashirofki-parolej-06-03",
            "uk": "https://telegra.ph/Process-zashirofki-parolej-06-03",
        }[lang]

        self.DECRYPT = {
            "en": "https://telegra.ph/Passwords-Decryption-Process-06-02",
            "ru": "https://telegra.ph/Process-deshifrovki-parolej-06-09",
            "uk": "https://telegra.ph/Process-deshifrovki-parolej-06-09",
        }[lang]

        self.GOOGLE_AUTH = {
            "en": "https://telegra.ph/Passcypher-Google-Authenticator-06-02",
            "ru": "https://telegra.ph/Passcypher-Ispolzovanie-Google-Authenticator-06-07",
            "uk": "https://telegra.ph/Passcypher-Ispolzovanie-Google-Authenticator-06-07",
        }[lang]


@lru_cache()
def links(lang) -> Links:
    return Links(lang)


def get_text(language, key):
    return texts[language][key]

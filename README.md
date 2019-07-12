# Passcypher_bot
Try this bot here: <a href="https://t.me/pcypher_bot"> @pcypher_bot</a>


This bot will help you <b>encrypt</b> your <b>passwords</b> to store them in <b>Telegram</b> (or wherever you want)<br>
Also you can <b>encrypt and decrypt</b> your <b>txt</b> files. 
However, don't put large txt files, please. 

This repository is created to show that bot does not store your passwords locally, and also you can make your commits to improve it.

New instruction:
https://telegra.ph/How-to-Use-Passcypher-Instruction-EN-06-02<br>
One more link is the instruction for Google Authenticator!
https://telegra.ph/Passcypher-Google-Authenticator-06-02

# New Features 12/07/2019
1. Added support i18n for translations
2. Made the use of standard filters of aiogram



# New Features
1. Updated to aiogram 2.0
2. Stated modified
3. Handlers separated
4. Statistics command
5. Use polling instead of Webhook
6. Added Ukrainian language
7. Bot now deletes user messages with passwords!

# Google Authenticator

Google authenticator feature has been added, so you won't need to enter your master password every time,
but instead, you'll be able to use Google authenticator app to unlock your passwords.


Download it here:<br>
App store link https://itunes.apple.com/gb/app/google-authenticator/id388497605?mt=8
<br>
Android link https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_GB

# gitignore

I've hidden a file with functions containing a small key which enables the extra level of security by a master password.
However, you can rename "secret.example.py" to "secret.py" and it will work

# Important!
You will need <b>Python 3.7+</b> to use this bot!

# How to use (WEBHOOK for advanced usage)

1. Clone the repository
2. Install the MYSQL on your server
3. Amend the config (and add needed variables to environment variables):
    -  Add bot token
    -  Your webhook host (you need to have the ssl enabled on it) 
    -  Bot port - port which receives the requests from telegram (For example, a nginx webserver redirecting requests from Telegram to 3000 port)
    -  Mysql database: user, password, db name
4. Install requirements <code>pip install -r requirements.txt</code>
5. <s>Run <code>python3.7 install.py</code> and follow the instructions</s> (Needs update)
6. Run <code>python3.7 main_bot.py</code>
 
 
# How to use (POLLING)

1. Clone the repository
2. Install the MYSQL on your server
3. Install requirements <code>pip install -r requirements.txt</code>
4. <s>Run <code>python3.7 install.py</code> and follow the instructions</s> (Needs update)
5. Run <code>python3.7 app.py</code>
 
# TODO
1. Configure the Docker 

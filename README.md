# Passcypher_bot


Try this bot here: <a href="https://t.me/pcypher_bot"> @pcypher_bot</a>


This bot will help you <b>encrypt</b> your <b>passwords</b> to store them in <b>Telegram</b> (or wherever you want)<br>
Also you can <b>encrypt and decrypt</b> your <b>txt</b> files. 
However, don't put large txt files, please. 

This repository is created to show that bot does not store your passwords locally, and also you can make your commits to improve it.

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


# How to use

1. Clone the repository
2. Change the config:
-  1. Add bot token
-  2. Your webhook host (you need to have the ssl enabled on it) 
-  3. Bot port - port which receives the requests from telegram (For example, a nginx webserver redirecting requests from Telegram to 3000 port)
-  4. Mysql database: user, password, db name
 3. Rename "secret.example.py" to "secret.py"
 4. Use sql.config to create a table in your database
 
 
# TODO
1. Add polling option for a faster installation
2. Move function blocks to separate files
3. Add Ukrainian language
4. Add statistics command.
5. Configure the Docker 

#!/usr/bin/env bash
echo "Installing updates"
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common -y
echo "Installing docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install docker-ce -y
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose
mv bot/utils/secret.example.py bot/utils/secret.py

echo "Compiling languages..."
pybabel extract bot/ -o locales/pcypher.pot
pybabel init -i locales/pcypher.pot -d locales -D pcypher -l en
pybabel init -i locales/pcypher.pot -d locales -D pcypher -l ru
pybabel init -i locales/pcypher.pot -d locales -D pcypher -l uk
pybabel compile -d locales -D pcypher

echo "Starting bot..."
sudo docker-compose up

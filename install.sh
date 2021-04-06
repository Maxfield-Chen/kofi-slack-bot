#!/bin/bash

function logging () {
    printf "=====================\n"
    printf "$1\n"
    printf "=====================\n"
}

if [ "$EUID" -ne 0 ]
then echo "Please run as root"
     exit
fi

logging "Configure your Ko-fi SlackBot."

read -p 'Enter Kofi Username: ' username
read -p 'Enter Slack Auth Token: ' authtoken
read -p 'Enter Channel Name: ' channel

logging "Installing dependencies..."

apt update
apt install --yes --force-yes python3 geckodriver git python3-venv

logging "Creating /tools/ Directory..."
mkdir /tools/
cd /tools/
logging "Cloning SlackBot Code..."
git clone https://github.com/Maxfield-Chen/kofi-slack-bot.git
logging "Installing Python Packages..."
cd kofi-slack-bot
python3 -m venv environment
. /tools/kofi-slack-bot/environment/bin/activate
pip install -r /tools/kofi-slack-bot/requirements.txt

logging "Setting up hourly crontab..."

echo -e "export SLACK_BOT_USER=$username\n" > /tools/kofi-slack-bot/environment-vars.sh
echo -e "export SLACK_BOT_TOKEN=$authtoken\n" > /tools/kofi-slack-bot/environment-vars.sh
echo -e "export SLACK_BOT_CHANNEL=$channel\n" > /tools/kofi-slack-bot/environment-vars.sh

cat /tools/kofi-slack-bot/crontab.txt >> /etc/crontab

logging "Changing file permissions to root to prevent security issues..."

chown root /tools/kofi-slack-bot/crontab.txt
chown root /tools/kofi-slack-bot/install.sh
chown root /tools/kofi-slack-bot/Main.py

chmod 600 /tools/kofi-slack-bot/crontab.txt
chmod 700 /tools/kofi-slack-bot/install.sh
chmod 700 /tools/kofi-slack-bot/Main.py

logging "All done! Make sure to check /etc/crontab and verify that your configuration is correct."

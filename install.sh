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
read -sp 'Enter Slack Auth Token: ' authtoken
read -p 'Enter Channel Name: ' channel

logging "Installing dependencies..."

apt update
apt install python3 geckodriver git

logging "Creating /tools/ Directory..."
mkdir /tools/
cd /tools/
logging "Cloning SlackBot Code..."
git clone git@github.com:Maxfield-Chen/kofi-slack-bot.git
cd kofi-slack-bot/
logging "Installing Python Packages..."
python3 -m venv environment
. ./environment/bin/activate
pip install -r ./requirements.txt

logging "Setting up hourly crontab..."

echo -e "SLACK_BOT_USER=$username\n$(cat /etc/crontab)" > /etc/crontab/
echo -e "SLACK_BOT_TOKEN=$authtoken\n$(cat /etc/crontab)" > /etc/crontab/
echo -e "SLACK_BOT_USER=$channel\n$(cat /etc/crontab)" > /etc/crontab/

cat ./crontab.txt >> /etc/crontab

logging "Changing file permissions to root to prevent security issues..."

chown root /tools/kofi-slack-bot/crontab.txt
chown root /tools/kofi-slack-bot/install.sh
chown root /tools/kofi-slack-bot/Main.py

chmod 600 /tools/kofi-slack-bot/crontab.txt
chmod 700 /tools/kofi-slack-bot/install.sh
chmod 700 /tools/kofi-slack-bot/Main.py

logging "All done! Make sure to check /etc/crontab and verify that your configuration is correct."

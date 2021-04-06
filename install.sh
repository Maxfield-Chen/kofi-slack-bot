#!/bin/bash

function logging () {
    printf "=====================\n"
    printf "$1\n"
    printf "=====================\n"
}

if [ "$EUID" -ne 0 ]
then echo "Please run as root so we can set crontabs."
     exit
fi

logging "Configure your Ko-fi SlackBot."

read -p 'Enter Running User Username: ' linuxuser
read -p 'Enter Kofi Username: ' username
read -p 'Enter Slack Auth Token: ' authtoken
read -p 'Enter Channel Name: ' channel

logging "Installing dependencies..."

apt update
apt install --yes --force-yes python3 git python3-venv firefox-geckodriver

logging "Creating /tools/ Directory..."
mkdir /tools/
chown $linuxuser /tools
cd /tools/

logging "Cloning SlackBot Code..."
git clone https://github.com/Maxfield-Chen/kofi-slack-bot.git

logging "Adding your user to the crontab..."
sed -i 's/maxfchen/$linuxuser/g' /tools/kofi-slack-bot/crontab.txt

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

logging "All done! Make sure to check /etc/crontab and verify that your configuration is correct."

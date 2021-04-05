# Kofi-Slack-Bot

A slack bot for [Ko-fi](https://ko-fi.com). The official Kofi slack bot will only report donations, this bot only reports new posts made on the creator's Kofi page.

![Example Message](https://maxfieldchen.com/images/kofi-slack-bot.png)

# Installation

First create a slack app by following these instructions:

  * [Slack App Basics](https://api.slack.com/authentication/basics)

Ensure you have a Slack authentication token, channel name, and Ko-fi creator name. You will need to grant this bot the `chat:write` privilege scope.

This bot comes with a install script that will start a cronjob as the root user to check for updates once an hour. This setup script can be run on the hosting provider of your choice using the following command:

`wget -qO- https://github.com/Maxfield-Chen/kofi-slack-bot/releases/download/v0.1/install.sh`

The configuration for this bot will be performed for you during the setup script run, but may also be performed by setting the following environment variables:

```
"SLACK_BOT_USER": kofi user (name, not URL).
"SLACK_BOT_TOKEN": Slack Authorization Token
"SLACK_BOT_CHANNEL": Controls which channel the bot posts to
```

💖 Made with love by Maxfield Chen 💖

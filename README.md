# kofi-slack-bot
A slack bot for [Ko-fi](https://ko-fi.com). The official Kofi slack bot will only report donations, this bot only reports new posts made on the creator's Kofi page.

![Example Message](https://maxfieldchen.com/images/kofi-slack-bot.png)

This bot comes with a install script that will start a cronjob as the root user to check for updates once an hour. This setup script can be run on the hosting provider of your choice using the following command:

``

The configuration for this bot can be performed by setting the following environment variables:

```
"SLACK_BOT_USER": kofi user (name, not URL).
"SLACK_BOT_TOKEN": Slack Authorization Token
"SLACK_BOT_CHANNEL": Controls which channel the bot posts to
```

💖 Made with love by Maxfield Chen 💖

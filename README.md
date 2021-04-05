# kofi-slack-bot
A slack bot for [Ko-fi](https://ko-fi.com). The official Kofi slack bot will only report donations, this bot only reports new posts made on the creator's Kofi page.

![Example Message](https://maxfieldchen.com/images/kofi-slack-bot.png)

This bot is dockerized and can be installed on the hosting service of your choice with the following command:

`docker to-do`

The configuration for this bot can be performed by setting the following environment variables:

```
"SLACK_BOT_USER": kofi user (name, not URL).
"SLACK_BOT_TOKEN": Slack Authorization Token
"SLACK_BOT_CHANNEL": Controls which channel the bot posts to
```

💖 Made with love by Maxfield Chen 💖

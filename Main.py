from selenium import webdriver
import os
import json
import sys
import typing
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Environment Variables
'''
"SLACK_BOT_USER": kofi user from URL.
"SLACK_BOT_TOKEN": slack authorization token.
"SLACK_BOT_CHANNEL": channel the bot will post in.
'''


serial_filename = "feed.json"
kofi_user = os.environ.get("SLACK_BOT_USER")
kofi_url = "https://ko-fi.com/" + kofi_user

def removeDonations(item: str) -> bool:
    if "bought a coffee" in item.lower():
        return False
    return True

def getNewItems(items: list[str]) -> list[str]:
    with open(serial_filename, "a+") as old_file:
        old_data = old_file.read()
        if not old_data: old_data = json.dumps({"feed": []})
        previous_items = json.loads(old_data)["feed"]
        new_items = []
        # Update serialized local json file, return new items
        if items != previous_items:
            serialized_items = json.dumps({"feed": items})
            with open(serial_filename, "w+") as serialize_file:
                serialize_file.write(serialized_items)
            new_items = [item for item in items if item not in previous_items]
        new_items = filter(removeDonations, new_items)
        return new_items


def getNewPosts(kofi_url: str) -> list[str]:
    new_items = []
    try:
        FirefoxOptions = webdriver.FirefoxOptions()
        FirefoxOptions.set_headless()
        driver = webdriver.Firefox(firefox_options=FirefoxOptions)
        driver.get(kofi_url)
        feed_items = list(map(lambda i: i.text, driver.find_elements_by_class_name("feeditem-unit")))
        new_items = getNewItems(feed_items)
    finally:
        try:
            driver.close()
        except:
            pass
    return new_items

def formatSlackMessage(message: str) -> str:
    kofi_message = "<" + kofi_url + "| New post on Kofi 👀>"
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "mrkdwn",
                "text":  kofi_message
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            }
        }
    ]
    return json.dumps(blocks)


def sendSlackMessage(message_block: str) -> bool:
    client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
    channel_id = os.environ.get("SLACK_BOT_CHANNEL")
    try:
        result = client.chat_postMessage(
            channel = channel_id,
            blocks = message_block
        )
    except SlackApiError as e:
        print(f"Error: {e}")
        return False
    return True


def main():
    new_items = getNewPosts(kofi_url)

    for message in new_items:
        message = formatSlackMessage(message)
        successful = sendSlackMessage(message)

if __name__ == "__main__":
    main()

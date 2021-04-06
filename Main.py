from selenium import webdriver
import os
import json
import sys
from typing import List
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
summary_word_count = 20
kofi_user = os.environ.get("SLACK_BOT_USER")
kofi_url = "https://ko-fi.com/" + kofi_user

def removeDonations(item: str) -> bool:
    if "bought a coffee" in item.lower():
        return False
    return True

def getNewItems(items: List[str]) -> List[str]:
    with open(serial_filename, "r+") as old_file:
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


def getNewPosts(kofi_url: str) -> List[str]:
    new_items = []
    try:
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=firefox_options)
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
    message_split = message.split("\n")
    message_title = message_split[2]
    message_body = message_split[3]
    message_summary = " ".join(message_body.split(" ")[:summary_word_count]) + ". . . ."
    blocks = [
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "There's a new post available on Kofi:"
			}
		},
		{
			"type": "section",
			"block_id": "kofi_post",
			"text": {
				"type": "mrkdwn",
				"text": ":eyes:<" + kofi_url + "|" + message_title + "> :eyes: \n " + message_summary
            },
            "accessory": {
                "type": "image",
                "image_url": "https://storage.ko-fi.com/cdn/useruploads/b8486e99-32fc-48e7-aba9-05eb3a2e92ea.png",
                "alt_text": "Kofi Brand Image"
            }
        },
        {
            "type": "divider"
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
        if message:
            message = formatSlackMessage(message)
            successful = sendSlackMessage(message)

if __name__ == "__main__":
    main()

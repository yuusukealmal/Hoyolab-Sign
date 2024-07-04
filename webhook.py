import os
import requests
import random

def parseres(result):
    blank = {"name": "** **", "value": "** **"}
    for i in range(len(result) - 1, 0, -1):
        result.insert(i, blank)
    return result

def webhook(results, time):
    webhook = os.environ.get('webhook_url')

    data = {
        "content": f"<@{os.environ.get('userid')}> Finish check-in at `{time}`",
        "embeds": 
        [
            {
                "title": "HoyoLab 簽到",
                "color": int("%06x" % random.randint(0, 0xFFFFFF), 16),
                "fields": parseres(results)
            }
        ],
        "username": "アストローギスト・モナ・メギストス",
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    result = requests.post(webhook, json=data, headers=headers)
    if 200 <= result.status_code < 300:
        print(f"Webhook sent {result.status_code}")
    else:
        print(f"Not sent with {result.status_code}, response:\n{result.json()}")
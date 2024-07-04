import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import webhook

ltuid = os.environ.get('ltuid_v2')
ltoken = os.environ.get('ltoken_v2')

class GAME:
    def __init__(self, name, domain, biz, act_id):
        self.name = name
        self.domain = domain
        self.biz = biz
        self.act_id = act_id

class METHOD:
    def __init__(self, name, method):
        self.name = name
        self.method = method

BASE = "https://sg-{}-api.hoyolab.com/event/{}/{}?act_id={}&lang=zh-tw" #domain, biz, method, act_id

games = [
    GAME("崩壞三", "public", "mani", "e202110291205111"),
    GAME("原神", "hk4e", "sol", "e202102251931481"),
    GAME("崩壞：星穹鐵道", "public", "luna/os", "e202303301540311"),
    GAME("絕區零", "act-nap", "luna/zzz/os", "e202406031448091")
]

methods = [
    METHOD("sign", "POST"),
    METHOD("info", "GET"),
    METHOD("home", "GET")
]

def req(method: METHOD, game: GAME, cookie=None):
    return requests.request(method.method, BASE.format(game.domain, game.biz, method.name, game.act_id), cookies=cookie).json()

def main():
    load_dotenv()

    ltuid = os.environ.get('ltuid_v2')
    ltoken = os.environ.get('ltoken_v2')

    cookies = {'ltuid_v2': ltuid, 'ltoken_v2': ltoken}

    results = []

    for game in games:
        r = req(methods[0], game, cookies)
        print(r)
        if r["retcode"] == -5003:
            results.append({"name": game.name, "value": r["message"]})

        if r["message"] == "OK":
            days = req(methods[1], game, cookies)["data"]["total_sign_day"]
            rewards = req(methods[2], game)["data"]["awards"][days-1]
            results.append({"name": game.name, "value": f'`{rewards["name"]}` x{rewards["cnt"]}'})

    time = datetime.utcnow() + timedelta(hours=8)

    webhook.webhook(results, time.strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    main()
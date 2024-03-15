import requests
import json
from config import dingding_token


class Dingding(object):
    def send(self, text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dingding_token
        json_text = self._msg(text)
        res = requests.post(api_url, json.dumps(json_text), headers=headers)
        # print(res)

    def _msg(self, text):
        json_text = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    "11111"
                ],
                "isAtAll": False
            },
            "text": {
                "content": "SOL_USDC: " + text
            }
        }
        return json_text

ding = Dingding()

if __name__ == "__main__":
    ding = Dingding()
    ding.send("sol")
    # https://oapi.dingtalk.com/robot/send?access_token=

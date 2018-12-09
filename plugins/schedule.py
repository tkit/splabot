from slackbot.bot import respond_to  # @botname: で反応するデコーダ
import re
import requests
import json
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')

BASE_URI = "https://spla2.yuu26.com/"


@respond_to('^リグマ$', re.IGNORECASE)
@respond_to('^リーグマッチ$', re.IGNORECASE)
@respond_to('^league$', re.IGNORECASE)
def respond_league_match_schedule(message):
    result = request_schedule("league")
    # 夜のスケジュールのみ抽出
    result = [a for a in result if a["start_jst"].hour in [1, 21, 23]]
    attachments = make_attachments(result, "リーグマッチ")
    message.send_webapi('夜のリーグマッチのスケジュールはこちらです♪', json.dumps(attachments))


@respond_to('^ガチマ$', re.IGNORECASE)
@respond_to('^ガチマッチ$', re.IGNORECASE)
@respond_to('^gachi$', re.IGNORECASE)
def respond_league_match_schedule(message):
    result = request_schedule("gachi")
    # 現在と次のスケジュールのみ抽出
    result = result[:2]
    attachments = make_attachments(result, "ガチマッチ")
    message.send_webapi('現在と次のガチマッチのスケジュールはこちらです♪', json.dumps(attachments))


def request_schedule(match_mode):
    if match_mode not in ["regular", "gachi", "league"]:
        # todo: error handling
        return

    try:
        r = requests.get("{}{}{}".format(BASE_URI, match_mode, "/schedule"))
    except Exception as e:
        print(e)
    return [{"rule": i["rule"], "maps": i["maps"],
             "start_jst": datetime.strptime(i["start_utc"], '%Y-%m-%dT%H:%M:%S%z').astimezone(JST)} for i in
            r.json()["result"]]


def make_attachments(mode_result, match_mode):
    if match_mode not in ["ナワバリバトル", "ガチマッチ", "リーグマッチ"]:
        # todo: error handling
        return
    att = [
        {
            "title": j["start_jst"].strftime('%Y/%m/%d %H:%M〜'),
            "fields": [
                {
                    "title": "ルール",
                    "value": j["rule"],
                    "short": True
                },
                {
                    "title": "ステージ",
                    "value": "\n".join(j["maps"]),
                    "short": True
                }
            ],
            "footer": "Splatoon2",
            "color": "good"
        } for j in mode_result
    ]
    return att

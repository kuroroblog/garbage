import datetime
import requests
import os

# 本日の日付を取得する。
def getToday():
    # timezoneを日本時間仕様に設定して、本日の日付を取得する。
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    # 一度本日の日付を整形して文字列型にし、再度date型へ変形する。
    return datetime.datetime.strptime(today.strftime('%Y-%m-%d'), '%Y-%m-%d')

# 本日の日付が◯曜日を基準とした場合に、第何週目の曜日なのか算出する関数
# https://note.nkmk.me/python-calendar-datetime-nth-dow/
# dt : 本日の日付
# firstWeekDay : 0~6, 0 : 月曜日, 1 : 火曜日, 2 : 水曜日, 3 : 木曜日, 4 : 金曜日, 5 : 土曜日, 6 : 日曜日, default : 月曜日
# response : int
def getNthWeek(dt, firstWeekDay=0):
    # 日にちを1に置換して月初のオブジェクトを生成し、weekday()メソッドで曜日のidx値を取得する。
    firstDow = dt.replace(day=1).weekday()
    # firstDow - firstWeekDay : -6~6
    # (割られる数) = (商) * (割る数) + (余り)
    # 7で割る理由は、1週間は7日であるため。
    # -6 = (-1) * 7 + 1
    # -5 = (-1) * 7 + 2
    # -4 = (-1) * 7 + 3
    # -3 = (-1) * 7 + 4
    # -2 = (-1) * 7 + 5
    # -1 = (-1) * 7 + 6
    #  0 =  (0) * 7 + 0
    #  1 =  (0) * 7 + 1
    #  2 =  (0) * 7 + 2
    #  3 =  (0) * 7 + 3
    #  4 =  (0) * 7 + 4
    #  5 =  (0) * 7 + 5
    #  6 =  (0) * 7 + 6
    # https://ja.stackoverflow.com/questions/66236/python-%E3%81%A7-%E8%B2%A0%E3%81%AE%E6%95%B0%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9F%E5%89%B0%E4%BD%99%E7%AE%97%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6
    offset = (firstDow - firstWeekDay) % 7
    # // : 切り捨て除算
    # idxの開始位置が0であるため、-1を行う。
    # + 1を行うのは、第0週から始まるのを防ぐため。
    return (dt.day + offset - 1) // 7 + 1

# 本日の日付が何曜日のidxに該当するのか演算する関数
# https://note.nkmk.me/python-calendar-datetime-nth-dow/
# dt : 本日の日付
# response : 0~6, 0 : 月曜日, 1 : 火曜日, 2 : 水曜日, 3 : 木曜日, 4 : 金曜日, 5 : 土曜日, 6 : 日曜日
def getNthDay(dt):
    # weekday()メソッドで曜日のidx値を取得する。
    return dt.weekday()

def garbage_test(event, context):
     monday = 0
     tuesday = 1
     wednesday = 2
     thursday = 3
     friday = 4
     saturday = 5
     sunday = 6

     infoList = {
          'burnable': {
               'message': '明日は燃やすゴミの日です',
               'days': [wednesday, saturday],
               'weeks': [],
          },
          'unburnable': {
               'message': '明日は燃やさないゴミの日です',
               'days': [sunday],
               'weeks': [2, 4],
          },
          'recyclable': {
               'message': '明日は資源ゴミの日です',
               'days': [monday],
               'weeks': [],
          },
     }

     today = datetime.date.today()
     message = ''
     for name, info in infoList.items():
          # offsetの設定は、日曜日を基準日とする。
          if getNthDay(today) in info['days'] and len(info['weeks']) == 0:
               message = info['message']
               break

          # offsetの設定は、日曜日を基準日とする。
          if getNthDay(today) in info['days'] and len(info['weeks']) > 0 and getNthWeek(today, 6) in info['weeks']:
               message = info['message']
               break

     if message:
          # 本番用トークンID
          lineNotifyToken = os.environ['token']
          # LINE Notify APIのURL
          lineNotifyApi = 'https://notify-api.line.me/api/notify'

          # Notify URL
          payload = {'message': message}
          headers = {'Authorization': 'Bearer ' + lineNotifyToken}
          requests.post(lineNotifyApi, data=payload, headers=headers)

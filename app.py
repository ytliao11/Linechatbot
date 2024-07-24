from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import requests
from waitress import serve

# 初始化 Flask 应用和 LINE Bot API
app = Flask(__name__)
line_bot_api = LineBotApi('UoTKrw0p7aNjTjcxy4mhKn4fB8ckub8uojTEtUDmD+TiPl5Gzs7e5qPaCBEFEgG5fILPue9HeiYc5OEhAnL8pjLQMGwtYqCF/8XUtSoFlg9zFyxbhobtamezlBjnPhyBWfYzWjNyh+M6nGpWgpDmDgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a42f467a09899053c37f640cd7e748cb')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if user_message == "一般車位":
        response = requests.get('https://script.google.com/macros/s/AKfycbzEWZvu8F6H98BDDzKSFf6iT0ykOpMYeeBqZwc95rqrodJCHWyxEtKH5lzm2z9-fhIUGg/exec')
        data = response.json()
        if data['status'] == 'success':
            last_record = data['data']
            remaining_slots = last_record[0][2]  # 假设最后一笔数据的格式为 [['一般車位', 69, 11, 58]]
            reply_message = f"一般車位剩餘:{remaining_slots}個空位"
        else:
            reply_message = "無法獲取數據。"
    elif user_message == "殘障車位":
        response = requests.get('https://script.google.com/macros/s/AKfycbw_A5VQZro0lXfldSyZkc4BY1n0rFIpqUIgy_wt7IEq0BGca37wdTL3kr2egmFJSqxOJg/exec')
        data = response.json()
        if data['status'] == 'success':
            last_record = data['data']
            remaining_slots = last_record[0][2] 
            reply_message = f"殘障車位剩餘:{remaining_slots}個空位"
        else:
            reply_message = "無法獲取數據。"
    elif user_message == "電動車位":
        response = requests.get('https://script.google.com/macros/s/AKfycbyg52yXA3ML7n9YpB8u4YrJ9o-4in6aFoFMV7wUjMdZZ3ifDX8EYKjH9ep4P3sxSVa4Sw/exec')
        data = response.json()
        if data['status'] == 'success':
            last_record = data['data']
            remaining_slots = last_record[0][2] 
            reply_message = f"電動車位剩餘:{remaining_slots}個空位"
        else:
            reply_message = "無法獲取數據。"
    else:
        reply_message = "請回答「一般車位」或「殘障車位」或「電動車位」。"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=3000)

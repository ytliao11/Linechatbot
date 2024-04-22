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
import pandas as pd  # Importing pandas to handle CSV files

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
        # Read the CSV file
        df = pd.read_csv('C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\output4.csvparkiinglot')  # Update the path to your CSV file
        # Get the last row of data as a string
        last_row = df.iloc[-1].to_string()
        reply_message = f"最後一筆資料：\n{last_row}"
    elif user_message == "殘障車位":
        reply_message = "目前沒有殘障車位的資料。"
    else:
        reply_message = "請回答「一般車位」或「殘障車位」。"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=3000)

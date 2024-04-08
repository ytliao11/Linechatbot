from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)
import requests
from waitress import serve

app = Flask(__name__)

line_bot_api = LineBotApi('UoTKrw0p7aNjTjcxy4mhKn4fB8ckub8uojTEtUDmD+TiPl5Gzs7e5qPaCBEFEgG5fILPue9HeiYc5OEhAnL8pjLQMGwtYqCF/8XUtSoFlg9zFyxbhobtamezlBjnPhyBWfYzWjNyh+M6nGpWgpDmDgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a42f467a09899053c37f640cd7e748cb')

@app.route("/callback", methods=['POST'])
def callback():
    # 從請求中獲取 X-Line-Signature 頭部，用於後續驗證
    signature = request.headers['X-Line-Signature']

    # 從請求中獲取請求主體
    body = request.get_data(as_text=True)

    # 處理 webhook 事件
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 根據用戶訊息決定要查詢的車位類型，並獲取對應的 Grafana 圖片 URL
    if user_message == "一般車位":
        image_url = "https://p0928367502.grafana.net/dashboard/snapshot/t3iI6XjPcR3gCLnXT3RnPMWIf8Rkwb25"
    elif user_message == "殘障車位":
        image_url = "GRAFANA_IMAGE_URL_FOR_DISABLED"
    else:
        reply_message = "請回答「一般車位」或「殘障車位」。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        return

    # 回覆圖片訊息
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
    )

if __name__ == "__main__":
      serve(app, host='0.0.0.0', port=3000)

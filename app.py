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
import pymysql.cursors
from waitress import serve

# 初始化 Flask 应用和 LINE Bot API
app = Flask(__name__)
line_bot_api = LineBotApi('UoTKrw0p7aNjTjcxy4mhKn4fB8ckub8uojTEtUDmD+TiPl5Gzs7e5qPaCBEFEgG5fILPue9HeiYc5OEhAnL8pjLQMGwtYqCF/8XUtSoFlg9zFyxbhobtamezlBjnPhyBWfYzWjNyh+M6nGpWgpDmDgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a42f467a09899053c37f640cd7e748cb')

# 数据库连接配置
connection = pymysql.connect(host='localhost:3306',
                             user='root',
                             password='qwe26600099',
                             database='parking',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

@app.route("/callback", methods=['POST'])
def callback():
    # 从请求中获取 X-Line-Signature 头，用于后续验证
    signature = request.headers['X-Line-Signature']

    # 从请求中获取请求主体
    body = request.get_data(as_text=True)

    # 处理 webhook 事件
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if user_message == "一般車位":
        with connection.cursor() as cursor:
            # 查询数据库中最后一条记录的详细信息
            cursor.execute("SELECT * FROM parkiinglot ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            # 构建返回的消息内容
            if result:
                reply_message = f"最后一条记录：{result}"
            else:
                reply_message = "没有找到相关的记录。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
    else:
        reply_message = "請回答「一般車位」或「殘障車位」。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

# 使用 Waitress 代替 Flask 自带的服务器，以提高生产环境下的性能和稳定性
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=3000)

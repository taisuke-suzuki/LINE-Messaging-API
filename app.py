import os

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn)

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["qP7rW14ZmINiO1l93FndzOLvCQEPh8mGKQ1xlfMIyqT8OUbRJLbUDddKJaMI23x7d/Gtd8ejp7dmrUD3ACABoM+U9bg39UjQizpnmxvR2Rld2E1a4itopz2WIwe2j+kB8ZgMI04fT3LXdX3wrx4mFwdB04t89/1O/w1cDnyilFU="]
LINE_CHANNEL_SECRET = os.environ["96805edc4dd3a51ee20dc515e8edc405"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()


#
# @handler.add(MessageEvent, message=TextMessage)
# def response_message(event):
#     if event.reply_token == "00000000000000000000000000000000":
#         return
#
#     # notesのCarouselColumnの各値は、変更してもらって結構です。
#     notes = [CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle02.jpg",
#                             title="【ReleaseNote】トークルームを実装しました。",
#                             text="creation(創作中・考え中の何かしらのモノ・コト)に関して、意見を聞けるようにトークルーム機能を追加しました。",
#                             actions=[{"type": "message","label": "サイトURL","text": "https://renttle.jp/notes/kota/7"}]),
#
#              CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle03.jpg",
#                             title="ReleaseNote】創作中の活動を報告する機能を追加しました。",
#                             text="創作中や考え中の時点の活動を共有できる機能を追加しました。",
#                             actions=[
#                                 {"type": "message", "label": "サイトURL", "text": "https://renttle.jp/notes/kota/6"}]),
#
#              CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle04.jpg",
#                             title="【ReleaseNote】タグ機能を追加しました。",
#                             text="「イベントを作成」「記事を投稿」「本を登録」にタグ機能を追加しました。",
#                             actions=[
#                                 {"type": "message", "label": "サイトURL", "text": "https://renttle.jp/notes/kota/5"}])]
#
#     messages = TemplateSendMessage(
#         alt_text='template',
#         template=CarouselTemplate(columns=notes),
#     )
#
#     line_bot_api.reply_message(event.reply_token, messages=messages)
#
#
# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)
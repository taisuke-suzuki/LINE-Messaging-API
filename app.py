import os

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, TextSendMessage, ButtonsTemplate, MessageAction)

app = Flask(__name__)

# LINE_CHANNEL_ACCESS_TOKEN = os.environ["qP7rW14ZmINiO1l93FndzOLvCQEPh8mGKQ1xlfMIyqT8OUbRJLbUDddKJaMI23x7d/Gtd8ejp7dmrUD3ACABoM+U9bg39UjQizpnmxvR2Rld2E1a4itopz2WIwe2j+kB8ZgMI04fT3LXdX3wrx4mFwdB04t89/1O/w1cDnyilFU="]
# LINE_CHANNEL_SECRET = os.environ["96805edc4dd3a51ee20dc515e8edc405"]
#
# line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# handler = WebhookHandler(LINE_CHANNEL_SECRET)

line_bot_api = LineBotApi("qP7rW14ZmINiO1l93FndzOLvCQEPh8mGKQ1xlfMIyqT8OUbRJLbUDddKJaMI23x7d/Gtd8ejp7dmrUD3ACABoM+U9bg39UjQizpnmxvR2Rld2E1a4itopz2WIwe2j+kB8ZgMI04fT3LXdX3wrx4mFwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("96805edc4dd3a51ee20dc515e8edc405")

@app.route("/")
def index():
    return "hello world!"


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
def response_message(event):
    # if event.reply_token == "00000000000000000000000000000000":
    #     return
    if event.message.text == "警察に連絡します":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="やめてくれええええ"))

    profile = line_bot_api.get_profile(event.source.user_id)

    messages = TemplateSendMessage(alt_text="詳細情報",
                                   template=ButtonsTemplate(
                                       thumbnail_image_url=profile.picture_url,
                                       title=profile.display_name,
                                       text="お前の見元はばればれだ！",
                                       actions=[MessageAction(label="困った", text="警察に連絡します")]))



    line_bot_api.reply_message(event.reply_token, messages=messages)
#

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from myclass.globals import GLOBALS
from myclass.requestHdlr import requestHdlr, postbackHdlr
from flask import Flask, request, abort, session

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent,
)

app          = Flask(__name__)
line_bot_api = LineBotApi(GLOBALS.YOUR_CHANNEL_ACCESS_TOKEN)
handler      = WebhookHandler(GLOBALS.YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('[MESSAGE] Dispatch event [%s] received at [%s] with token [%s]'%(event.message.type, event.timestamp, event.reply_token))
    requestHandler = requestHdlr(event, handler, line_bot_api)
    if event.source.type == 'group' and event.source.group_id in GLOBALS.WHITE_LIST:
        requestHandler.setWhiteList(True)
    requestHandler.dispatch()

@handler.add(PostbackEvent)
def handle_postback(event):
    print('[POSTBACK] Dispatch [%s] received at [%s] with token [%s]'%(event.postback.data, event.timestamp, event.reply_token))
    requestHandler = postbackHdlr(event, handler, line_bot_api)
    if event.source.type == 'group' and event.source.group_id in GLOBALS.WHITE_LIST:
        requestHandler.setWhiteList(True)
    requestHandler.dispatch()

if __name__ == "__main__":
    app.run()
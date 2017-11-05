from myclass.globals import GLOBALS
from myclass.requestHdlr import requestHdlr
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, 
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
    requestHandler = requestHdlr(event, handler, line_bot_api)
    # Do filter and logger
    if event.source.type == 'group':
        print( 'Get message from group %s.'%(event.source.group_id) )
        if event.source.group_id in GLOBALS.WHITE_LIST:
            requestHandler.setWhiteList(True)
    elif event.source.type == 'room':
        print( 'Get message from room %s.'%(event.source.room_id) )
    elif event.source.type == 'user':
        print( 'Get message from user %s.'%(event.source.user_id) )    

    requestHandler.dispatch()

if __name__ == "__main__":
    app.run()
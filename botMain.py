import base64,requests
from io import BytesIO
from myclass.firebaseWrapper import firebaseWrapper
from myclass.globals import GLOBALS
from myclass.requestHdlr import requestHdlr, postbackHdlr
from flask import Flask, request, abort, session, send_file

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent,
    ImageMessage, TextMessage, 
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

@app.route("/googlemap")
def send_image():
    center     = request.args.get('center')
    markers    = request.args.get('markers')

    fb         = firebaseWrapper(GLOBALS.DATABASE_BASE_URL)
    token      = request.args.get('token')

    if fb.has_one('funnyBot/gmap_token',token):
        fb.delete_one('funnyBot/gmap_token',token)
    else:
        return 'Page not found'

    url = 'https://maps.googleapis.com/maps/api/staticmap'
    params = {
        'center'   : center,
        'zoom'     : 15,
        'size'     : '300x316',
        'language' : 'zh-tw',
        'markers'  : markers
    }
    obj_page = requests.get(url, params=params)
    with open('%s.png'%token, 'wb') as f:
        for chunk in obj_page:
            f.write(chunk)

    return send_file('%s.png'%token, mimetype='image/png')

@handler.add(MessageEvent)
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

@handler.default()
def default(event):
    print('Drop event [%s] received at [%s] with token [%s]'%(event.type, event.timestamp, event.reply_token))

if __name__ == "__main__":
    app.run()
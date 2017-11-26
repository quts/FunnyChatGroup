import flask,requests, logging, sys

from myclass.firebaseWrapper import firebaseWrapper
from myclass.globals import GLOBALS
from myclass.requestHdlr import requestHdlr, postbackHdlr

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

app = flask.Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

line_bot_api = LineBotApi(GLOBALS.YOUR_CHANNEL_ACCESS_TOKEN)
handler      = WebhookHandler(GLOBALS.YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = flask.request.headers['X-Line-Signature']

    # get request body as text
    body = flask.request.get_data(as_text=True)
    app.logger.info(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        flask.abort(400)

    return 'OK'

@handler.add(MessageEvent)
def handle_message(event):
    app.logger.info('Dispatch event [%s] received at [%s] with token [%s] >>>'%(event.message.type, event.timestamp, event.reply_token))
    requestHandler = requestHdlr(event, handler, line_bot_api)
    if event.source.type == 'group' and event.source.group_id in GLOBALS.WHITE_LIST:
        requestHandler.setWhiteList(True)
    requestHandler.dispatch()
    app.logger.info('<<<')

@handler.add(PostbackEvent)
def handle_postback(event):
    app.logger.info('Dispatch [%s] received at [%s] with token [%s] >>>'%(event.postback.data, event.timestamp, event.reply_token))
    requestHandler = postbackHdlr(event, handler, line_bot_api)
    if event.source.type == 'group' and event.source.group_id in GLOBALS.WHITE_LIST:
        requestHandler.setWhiteList(True)
    requestHandler.dispatch()
    app.logger.info('<<<')

@handler.default()
def default(event):
    app.logger.info('Drop event [%s] received at [%s] with token [%s] >>>'%(event.type, event.timestamp, event.reply_token))
    app.logger.info('<<<')

@app.route("/")
def helloworld():
    return 'Hello World!!'


@app.route("/googlemap")
def send_image():
    center     = flask.request.args.get('center')
    markers    = flask.request.args.get('markers')

    fb         = firebaseWrapper(GLOBALS.DATABASE_BASE_URL)
    token      = flask.request.args.get('token')

    fb.set_db(GLOBALS.DATABASE_BASE_NAME)

    if fb.has_one('gmap_token',token):
        data = fb.get_key('gmap_token/%s'%token)
        print(data)
        for item in data['request']:
            if '%s,%s'%(item['lat'],item['lng']) == center and markers == item['name']:
                app.logger.debug('Requested item exists!!')
                url = 'https://maps.googleapis.com/maps/api/staticmap'
                params = {
                    'center'   : center,
                    'zoom'     : 15,
                    'size'     : '300x316',
                    'language' : 'zh-tw',
                    'markers'  : markers
                }
                obj_page = flask.requests.get(url, params=params)
                with open('%s.png'%token, 'wb') as f:
                    for chunk in obj_page:
                        f.write(chunk)

                return flask.send_file('%s.png'%token, mimetype='image/png')

    app.logger.info('Requested item [%s] not exists in [%s] from [%s]'%(center,token,flask.request.remote_addr))
    return 'Have a nice day'

if __name__ == "__main__":
    app.run()




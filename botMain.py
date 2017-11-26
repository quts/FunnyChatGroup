import flask, requests, logging, sys

from myclass.firebaseWrapper import firebaseWrapper
from myclass.globals import GLOBALS
from myclass.requestHdlr import requestHdlr, postbackHdlr
from myclass.errorcode import CommonError

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
    '''
    Main function of the chatbot which process callback from line server
    '''

    # get X-Line-Signature header value
    signature = flask.request.headers['X-Line-Signature']

    # get request body as text
    body = flask.request.get_data(as_text=True)
    app.logger.debug(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        flask.abort(400)

    return 'OK'

@handler.add(MessageEvent) 
def handle_message(event):
    '''
    Message event hander
    '''
    app.logger.info('>>> Dispatch [%s] event [%s] received at [%s] with token [%s]'%(event.type, event.message.type, event.timestamp, event.reply_token))
    requestHandler = requestHdlr(event, handler, line_bot_api)
    if event.source.type == 'group' and event.source.group_id in GLOBALS.WHITE_LIST:
        requestHandler.setWhiteList(True)
    requestHandler.dispatch()
    app.logger.info('<<<')

@handler.add(PostbackEvent) 
def handle_postback(event):
    '''
    postback event hander
    '''
    app.logger.info('>>> Dispatch [%s] event [%s] received at [%s] with token [%s]'%(event.type, event.postback.data, event.timestamp, event.reply_token))
    requestHandler = postbackHdlr(event, handler, line_bot_api)
    if event.source.type == 'group' and event.source.group_id in GLOBALS.WHITE_LIST:
        requestHandler.setWhiteList(True)
    requestHandler.dispatch()
    app.logger.info('<<<')

@handler.default()
def default(event): 
    '''
    drop non-interest event hander
    '''
    app.logger.info('>>> Drop event [%s] received at [%s] with token [%s]'%(event.type, event.timestamp, event.reply_token))
    app.logger.info('<<<')

@app.route("/") # drop non-interest event hander
def helloworld():
    return CommonError.PAGE_NOT_FOUND.get_msg()


@app.route("/googlemap")
def send_image():
    '''
    Handle request come from http/https directly.
    Will verify if requested data exists in database inorder to avoid attack
    User who want to get google map image via this function should call location event first
    Location event handler will insert data to database

    Note : Not to delete data from database immediatly to avoid image not found issue in chatroom/chatgroup
    '''
    center     = flask.request.args.get('center')
    markers    = flask.request.args.get('markers')

    fb         = firebaseWrapper(GLOBALS.DATABASE_BASE_URL)
    token      = flask.request.args.get('token')

    fb.set_db(GLOBALS.DATABASE_BASE_NAME)

    if fb.has_one('gmap_token',token):
        data = fb.get_key('gmap_token/%s'%token)
        for item in data['requests']:
            if item['center'] == center and item['name'] in markers:
                app.logger.debug('>>> Requested item [%s] found in [%s] from [%s]'%(center,token,flask.request.remote_addr))
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

                return flask.send_file('%s.png'%token, mimetype='image/png')

    app.logger.info('<<< Requested item [%s] not exists in [%s] from [%s]'%(center,token,flask.request.remote_addr))
    return CommonError.PAGE_NOT_FOUND.get_msg()

if __name__ == "__main__":
    '''
    The main function is call by python directly
    Usually, heroku will call gunicorn to launch the script, and this part will not be invoked!
    '''
    app.run()




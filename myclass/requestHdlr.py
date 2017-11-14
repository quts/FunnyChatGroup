import os, random
from urllib.parse import parse_qs
from myclass.firebaseWrapper import firebaseWrapper
from myclass.globals import GLOBALS, MESSAGE
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
)

class requestHdlr(object):
    def __init__(self, event, handler, line_bot_api):
        self._event = event
        self._hdlr  = handler
        self._line  = line_bot_api
        self._inlist= False

    def setWhiteList(self, bSwitch):
        self._inlist = bSwitch

    def dispatch(self):
        if self._event.message.type == 'text':
            self.string_command_handler()

    def string_command_handler(self):
        if GLOBALS.YOUR_NAME_OF_THE_BOT in self._event.message.text:
            self._replyText(u'有人在找%s嗎？'%GLOBALS.YOUR_NAME_OF_THE_BOT)
        
        elif self._event.message.text == u'抽' or self._event.message.text == 'pick':
            luck_number = random.choice(range(0,100))
            if(luck_number == 87 or not self._inlist):
                self._replyText(MESSAGE.LUCKY_MESSAGE)
            else:
                fb              = firebaseWrapper(GLOBALS.DATABASE_BASE_URL)
                lst_target_list = fb.fb.get(GLOBALS.DATABASE_BASE_NAME, GLOBALS.DATABASE_PAGE_RANDOM_PICKED)
                random_picked   = random.choice(list(lst_target_list.keys()))
                if lst_target_list[random_picked]['type'] == 'photo':
                    self._replyImage( lst_target_list[random_picked]['url'] )
        
        elif self._event.message.text == u'ok,bot':
            self._replyText(MESSAGE.WHAT_CAN_I_DO)

        elif self._event.message.text == u'ok,telladmin':
            self._replySenderInfo()

        elif self._event.message.text == u'ok,lang':
            self._set_language()

    def _replyImage(self, image_url):
        self._line.reply_message(
                self._event.reply_token,
                ImageSendMessage(
                        original_content_url=image_url,
                        preview_image_url=image_url
                    )
            )

    def _replyText(self, msg):
        #self._event.message.text
        self._line.reply_message(
                self._event.reply_token,
                TextSendMessage(
                        text=msg
                    )
            )

    def _replySenderInfo(self):
        user_id   = 'undef'
        user_type = 'undef'
        if self._event.source.type == 'group':
            user_id   = self._event.source.group_id
            user_type = 'group'
        elif self._event.source.type == 'room':
            user_id   = self._event.source.room_id
            user_type = 'room'
        elif self._event.source.type == 'user':
            user_id   = self._event.source.room_id
            user_type = 'room'
        self._replyText('id[%s]\ntype[%s]\nstatus[%s]'%(user_id,user_type,self._inlist))

    def _set_language(self):
        self._line.reply_message(
            self._event.reply_token,
            TemplateSendMessage(
                alt_text='CHANGE LANGUAGE SETTING',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://example.com/image.jpg',
                    title='CHANGE LANGUAGE SETTING',
                    text='Which one do you want?',
                    actions=[
                        PostbackTemplateAction(
                            label='English',
                            data='action=setlang&value=en_us'
                        ),
                        PostbackTemplateAction(
                            label=u'中文',
                            data='action=setlang&value=zh_tw'
                        )
                    ]
                )
            )
        )

class postbackHdlr(requestHdlr):

    def dispatch(self):
        dict_request = parse_qs(self._event.postback.data)
        if 'setlang' in dict_request['action']:
            if 'zh_tw' in dict_request['value']:
                self._replyText(u'那就讓我們說中文吧！')
            elif 'en_us' in dict_request['value']:
                self._replyText('Let us talk in English')
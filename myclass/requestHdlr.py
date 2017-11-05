import os, random

from myclass.firebaseWrapper import firebaseWrapper
from myclass.globals import GLOBALS, MESSAGE
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
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
        if GLOBALS.YOUR_NAME_OF_THE_BOT in self._event.message.text:
            self._replyText(u'有人在找%s嗎？'%GLOBALS.YOUR_NAME_OF_THE_BOT)
        
        elif self._event.message.text == u'抽':
            luck_number = random.choice(range(0,100))
            if(luck_number == 87 or not self._inlist):
                self._replyText(MESSAGE.LUCKY_MESSAGE)
            else:
                fb              = firebaseWrapper(GLOBALS.DATABASE_BASE_URL)
                lst_target_list = fb.fb.get(GLOBALS.DATABASE_BASE_NAME, GLOBALS.DATABASE_PAGE_RANDOM_PICKED)
                random_picked   = random.choice(list(lst_target_list.keys()))
                self._replyImage( lst_target_list[random_picked]['url'] )

        elif self._event.message.text == u'ok,bot':
            self._replyText(MESSAGE.WHAT_CAN_I_DO)

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
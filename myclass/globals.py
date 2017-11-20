import os

class GLOBALS:
    YOUR_CHANNEL_ACCESS_TOKEN   = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
    YOUR_CHANNEL_SECRET         = os.environ['YOUR_CHANNEL_SECRET']
    YOUR_NAME_OF_THE_BOT        = u'%s'%os.environ['YOUR_NAME_OF_THE_BOT']

    DATABASE_BASE_URL           = os.environ['DATABASE_BASE_URL']
    DATABASE_BASE_NAME          = os.environ['DATABASE_BASE_NAME']
    DATABASE_PAGE_RANDOM_PICKED = os.environ['DATABASE_PAGE_RANDOM_PICKED']

    WHITE_LIST                  = [ item.strip() for item in os.environ['WHITE_LIST'].split(',')] if 'WHITE_LIST' in os.environ else None

class MESSAGE:
    WHAT_CAN_I_DO = u"你好我是%s\n"%(GLOBALS.YOUR_NAME_OF_THE_BOT) + \
                    u"輸入[抽]或是[pick]我會抽籤給你看\n" + \
                    u"輸入[ok,bot]我會告訴你我會什麼\n"
    HELLO_WORLD   = u"Hello World 歡迎光臨"
    LUCKY_MESSAGE = u"哈囉～肥宅～想幹嘛啊！"

    POST_BACK_ALT = u"請在手機上選擇 Select on Mobile"

    PLEASE_SELECT = u"請選擇 Please Select"
    AGREE         = u"同意 Agree"
    DISAGREE      = u"不同意 Disagree"

    DONATE_IMAGE  = u"謝謝你與我分享這張照片，請問你擁有這張照片的版權且同意授權%s與其他所有用戶分享嗎？"%(GLOBALS.YOUR_NAME_OF_THE_BOT)

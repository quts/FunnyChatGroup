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
                    u"輸入[抽]我會抽籤給你看\n" + \
                    u"輸入[ok,bot]我會告訴你我會什麼\n"
    HELLO_WORLD   = u"Hello World 歡迎光臨"
    LUCKY_MESSAGE = u"哈囉～肥宅～想幹嘛啊！"
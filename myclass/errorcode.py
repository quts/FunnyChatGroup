class MakeError(Exception):
    def __init__(self, code_type, module, code, msg):
        self.code = code_type<<15 + module<<13 + code
        self.msg  = msg

    def get_code(self):
        return self.code

    def get_msg(self):
        return self.msg

    def __str__(self):
        return repr(self.code)

class CommonError:
    SUCCESS             = 0x2
    ERROR               = 0x1

    SETTING_ERROR       = 0x1
    NO_HOST_OR_NO_BOARD = MakeError( ERROR, SETTING_ERROR, 0x1, 'Host and board name are must be set' )
    NO_EXTENSION_IN_ENV = MakeError( ERROR, SETTING_ERROR, 0x2, 'Have to set environment variable for interest extesion' )

    POST_BACK_IMAGE     = 0x2
    AGREE_TO_DONATE     = MakeError( SUCCESS, POST_BACK_IMAGE, 0x1, 'User Agree To Donate The Image' )
    DISAGREE_TO_DONATE  = MakeError( SUCCESS, POST_BACK_IMAGE, 0x2, 'User Disagree To Donate The Image' )

    LOCATION_EVENT_HDLR = 0x3
    NO_AVALIABLE_DATA   = MakeError( ERROR, LOCATION_EVENT_HDLR, 0x1, 'Unknown error happen, please try again' )

    HTTP_ERROR          = 0xff
    PAGE_NOT_FOUND      = MakeError( ERROR, HTTP_ERROR, 0x1, 'Have a nice day :)' )
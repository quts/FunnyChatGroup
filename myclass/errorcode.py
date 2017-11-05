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
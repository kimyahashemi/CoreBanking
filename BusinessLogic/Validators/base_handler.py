from .ihandler import IHandler


class BaseHandler(IHandler):
    def __init__(self):
        self.__next_handler=None
        
    def set_next(self, next_handler):
        self.__next_handler = next_handler

    def validate(self, request):
        if self.__next_handler:
            self.__next_handler.validate(request)

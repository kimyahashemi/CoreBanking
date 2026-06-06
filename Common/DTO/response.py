class Response:
    def __init__(self, success:bool, message:str, data):
        self.success = success
        self.message = message
        self.data = data
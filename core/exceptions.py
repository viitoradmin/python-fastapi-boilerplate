class CustomException(Exception):

    def __init__(self, status, data, message):
        self.status = status
        self.data = data
        self.message = message

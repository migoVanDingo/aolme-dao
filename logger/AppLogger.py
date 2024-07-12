from flask import current_app
class AppLogger:
    def __init__(self)->None:
        pass
        

    def log(self, message):
        current_app.logger.debug(message)



class BaseException(Exception):
    def __init__(self, position_start, position_end, error_type: str, message: str):
        self.position_start = position_start
        self.position_end = position_end
        self.error_type = error_type
        self.message = message

    def to_string(self):
        return f"{self.error_type}: {self.message}\n" + \
            f"File: {self.position_start.filename}, line: {self.position_end.line}"

class IllegalCharacterException(BaseException):
    def __init__(self, position_start, position_end, message: str):
        super().__init__(position_start, position_end, self.__class__.__name__, message)

class InvalidSyntaxError(BaseException):
    def __init__(self, position_start, position_end, message: str):
        super().__init__(position_start, position_end, self.__class__.__name__, message)
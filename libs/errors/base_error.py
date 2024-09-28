
class BaseError(Exception):

    def __init__(self, _message, _error=None, _source=None,):

        self.message = _message
        self.source = _source
        self.error = _error

        super().__init__(_message)

    def __get_FullMsgError(self):
        value = f'{self.message}'
        if self.source:
            value = f'{value} ({self.source})'

        if self.error:
            value = f'{value}: {self.error}'

        return value

    def __str__(self):
        return self.__get_FullMsgError()

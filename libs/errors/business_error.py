# errors
from libs.errors.base_error import BaseError


class BusinessError(BaseError):
    pass


class NotRelatedError(BaseError):
    pass

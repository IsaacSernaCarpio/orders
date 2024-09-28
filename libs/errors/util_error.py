# errors
from libs.errors.base_error import BaseError


class UtilError(BaseError):
    pass


class ParameterNotFoundError(BaseError):
    pass


class NullParameterError(BaseError):
    pass

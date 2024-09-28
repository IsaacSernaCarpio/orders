import re

# errors
from libs.errors.util_error import UtilError


class RegexValidator(object):

    @classmethod
    def validate_phone(self, _value):
        try:
            pattern = '^[A-Z0-9]{10,15}$'
            result = re.match(pattern, _value)

            return result

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e)
            )

    @classmethod
    def validate_letters_numbers(self, _value):
        try:
            pattern = '^[a-zA-Z0-9]$'
            result = re.match(pattern, _value)

            return result

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e)
            )

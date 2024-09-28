# enum
from enum import Enum


class FilterOperator(Enum):
    CONTAINS = "contains"
    IS_NOT = "isNot"
    STARTSWITH = "startsWith"
    ENDSWITH = "endsWith"
    ISEMPTY = "isEmpty"
    NOTEMPTY = "isNotEmpty"
    EQUALS = "="
    NOTEQUAL = "!="
    GRTHAN = ">"
    GREQTHAN = ">="
    LRTHAN = "<"
    LREQTHAN = "<="
    IN = "in"
    NOT_IN = "not_in"
    IS = "is"

    @staticmethod
    def list():
        return list(map(lambda item: item, FilterOperator))

    @staticmethod
    def value_list():
        return list(map(lambda item: item.value, FilterOperator))


class FilterField(object):

    def __init__(self, _field_name, _operator, _value):
        self.field_name = _field_name
        self.operator = _operator
        self.value = _value


class FiltersDTO(list):

    def fill(self, _list_filter):
        self.extend(_list_filter)

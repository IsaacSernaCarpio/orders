# errors
from libs.errors.util_error import UtilError
from libs.errors.dao_error import DaoError

# filters
from libs.filters.filters_base import FilterOperator


class FiltersDao(object):

    def __init__(self, _model, _filters_dto):
        self.model = _model
        self.filters_dto = _filters_dto

    def validate_ifmodelhasfilters(self):
        if self.model is None:
            return False

        model_filters = self.model.get_dict(_nulls=False)
        return bool(model_filters)

    def validate_iffilterdtohasvalues(self):
        if self.filters_dto is None:
            return False

        if len(self.filters_dto) > 0:
            return True

        else:
            return False

    def check_thatfiltersarenotnull(self):
        model_filters_flag = self.validate_ifmodelhasfilters()
        custom_filters_flag = self.validate_iffilterdtohasvalues()

        if model_filters_flag is False and custom_filters_flag is False:
            raise DaoError("some filter should be specified")

        return True

    def get_filter(self, _model, _field_name, _type, _value):
        if _type not in FilterOperator.list():
            raise UtilError(f"Operator Type {_type} don't exist")

        if isinstance(_model, self.model.__class__):
            model_name = self.model.__class__
        else:
            model_name = _model

        if _type == FilterOperator.CONTAINS:
            return getattr(model_name, _field_name).contains(_value)

        if _type == FilterOperator.IS_NOT:
            return getattr(model_name, _field_name).isnot(_value)

        if _type == FilterOperator.STARTSWITH:
            return getattr(model_name, _field_name).startswith(_value)

        if _type == FilterOperator.ENDSWITH:
            return getattr(model_name, _field_name).endswith(_value)

        if _type == FilterOperator.IS:
            return getattr(model_name, _field_name).is_(_value)

        if _type == FilterOperator.ISEMPTY:
            return getattr(model_name, _field_name).is_(None)

        if _type == FilterOperator.NOTEMPTY:
            return getattr(model_name, _field_name).isnot(None)

        if _type == FilterOperator.EQUALS:
            return getattr(model_name, _field_name).__eq__(_value)

        if _type == FilterOperator.IN:
            return getattr(model_name, _field_name).in_(_value)

        if _type == FilterOperator.NOT_IN:
            return getattr(model_name, _field_name).notin_(_value)

        if _type == FilterOperator.NOTEQUAL:
            return getattr(model_name, _field_name).__ne__(_value)

        if _type == FilterOperator.GRTHAN:
            return getattr(model_name, _field_name).__gt__(_value)

        if _type == FilterOperator.GREQTHAN:
            return getattr(model_name, _field_name).__ge__(_value)

        if _type == FilterOperator.LRTHAN:
            return getattr(model_name, _field_name).__lt__(_value)

        if _type == FilterOperator.LREQTHAN:
            return getattr(model_name, _field_name).__le__(_value)

        raise UtilError(f"Operator Type {_type} without definition")

    def get_modelfilterslist(self):
        filters_list = []

        if self.model is None:
            return []

        data_filters = self.model.get_dict(_nulls=False)

        for key, value in data_filters.items():
            filters_list.append(self.get_filter(
                self.model,
                key,
                FilterOperator.EQUALS,
                value
            ))

        return filters_list

    def get_customfilterlist(self):

        filters_list = []

        if self.filters_dto is None or len(self.filters_dto) == 0:
            return filters_list

        for filter in self.filters_dto:
            filters_list.append(
                self.get_filter(
                    self.model,
                    filter.field_name,
                    filter.operator,
                    filter.value
                )
            )

        return filters_list

    def build_filters(self):
        model_filters_list = self.get_modelfilterslist()
        custom_filters_list = self.get_customfilterlist()

        filters_list = model_filters_list + custom_filters_list

        return filters_list

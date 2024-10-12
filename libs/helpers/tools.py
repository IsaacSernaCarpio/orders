# python libraries
import re
import math

# fastapi
from fastapi import HTTPException

# datetime
from datetime import datetime

# settings
from settings import PWD_CONTEXT

# errors
from libs.errors.business_error import BusinessError

# filters
from libs.filters.filters_base import FilterOperator

operators_dict = {
    "contains": FilterOperator.CONTAINS,
    "equals": FilterOperator.EQUALS,
    # "isNot": FilterOperator.NOTEQUAL,
    # "startsWith": FilterOperator.STARTSWITH,
    # "endsWith": FilterOperator.ENDSWITH,
    # "isEmpty": FilterOperator.ISEMPTY,
    # "isNotEmpty": FilterOperator.NOTEMPTY,
    # "in": FilterOperator.IN,
    # "not_in": FilterOperator.NOT_IN,
    # "=": FilterOperator.EQUALS,
    # "!=": FilterOperator.NOTEQUAL,
    # ">": FilterOperator.GRTHAN,
    # ">=": FilterOperator.GREQTHAN,
    # "<": FilterOperator.LRTHAN,
    # "<=": FilterOperator.LREQTHAN,
    # "is": FilterOperator.IS
}


class Tools(object):

    @classmethod
    def get_links_mysql(
        self,
        _path_url,
        _page,
        _limit, 
        _total_rows
    ):
        base_url = f"/{_path_url}?limit={_limit}?page"

        links = {}
        links['total_rows'] = _total_rows
        links['total_pages'] = math.ceil(_total_rows / _limit)
        links['first_page'] = 1
        links['current_page'] = _page
        links['last_page'] = links['total_pages']
        links['after_page'] = None
        links['before_page'] = None

        links['before_page'] = links['current_page'] - 1

        if links['current_page'] < links['total_pages']:
            links['after_page'] = links['current_page'] + 1

        links_data = {}
        
        links_data['self'] = f"{base_url}={links['current_page']}"
        links_data['first'] = f"{base_url}={links['first_page']}"

        if links['before_page']:
            links_data['prev'] = f"{base_url}={links['before_page']}"

        if links['after_page']:
            links_data['next'] = f"{base_url}={links['after_page']}"

        links_data['last'] = f"{base_url}={links['last_page']}"

        return links_data

    @classmethod
    def add_links_path(
        cls,
        _links,
        _filter_column,
        _filter_operator,
        _filter_value
    ):
        url = f"&filter_column={_filter_column}&filter_operator={_filter_operator}&filter_value={_filter_value}"
        if _filter_column:
            for path in _links:
                _links[path] = f"{_links[path]}{url}" 

        return True

    @classmethod
    def get_links_mongo(
        cls,
        _path_url,
        _offset,
        _limit, 
        _total_rows
    ):
        links = {}
        end_document = _offset + _limit
        total_pages = _total_rows / _limit

        if end_document < _total_rows:
            if _offset > 1:
                links["previous"] = f"/{_path_url}?offset={_offset-1}&limit={_limit}"
            else:
                links["previous"] = None
            
            links["next"] = f"/{_path_url}?offset={_offset+1}&limit={_limit}"

        else:
            if _offset > 1:
                links["previous"] = f"/{_path_url}?offset={_offset-1}&limit={_limit}"
            else:
                links["previous"] = None
            
            links["next"] = None
            if end_document == _total_rows:
                links["next"] = f"/{_path_url}?offset={_offset+1}&limit={_limit}"
            
            if _offset > total_pages:

                links["previous"] = None
        
        return links

    @classmethod
    def get_url_retrieve(cls,  _path_url, _id):
        return {
            "url": f"/{_path_url}/{_id}"
        }

    @classmethod
    def check_sortcolumn(cls, _sort_column, _options_list):
        if _sort_column not in _options_list:
            error_message = f"sortColumn: {_sort_column} not valid"
            raise HTTPException(error_message, 400)

        return True
    
    @classmethod
    def check_sorttype(cls, _sort_type):
        options_list = ['DESC', 'ASC']
        if _sort_type in options_list:
            error_message = f"sortType: {_sort_type} not valid"
            raise HTTPException(error_message, 400)

        return True
    
    def check_page_and_size(
        self,
        _page=None,
        _size=None
    ):
        if _page is None:
            return 1, 10
        
        # Calcular el índice de inicio y fin para la paginación
        start_index = (_page - 1) * _size
        end_index = start_index + _size

        return start_index, end_index

    def check_phone_number_by_regex(self, _phone_numer):
        phone_numer = str(_phone_numer)
        # Expresión regular para validar números de teléfono celular en México
        patron_mexicano = re.compile(r'^\d{10}$')

        # Validar el número usando la expresión regular
        es_valido = bool(patron_mexicano.match(phone_numer))
        
        return es_valido

    def check_date_in_range(
        self,
        _fecha_a_comparar,
        _fecha_inicio,
        _fecha_fin
    ):
        
        return _fecha_inicio <= _fecha_a_comparar <= _fecha_fin

    def validate_date_greaterthan_thecurrentone(
        self,
        _date
    ):
        fecha_utc_actual = datetime.now()
        if _date <= fecha_utc_actual:
            msg = "La fecha y hora deben ser mayores que el momento actual"
            raise ValueError(msg)
        
        return _date

    def set_hash(self, _text_plane):
        return PWD_CONTEXT.hash(_text_plane)
    
    @classmethod
    def get_month_name(cls,  _month_number):
        month_dict = {
            1: 'Enero',
            2: 'Febrero',
            3: 'Marzo',
            4: 'Abril',
            5: 'Mayo',
            6: 'Junio',
            7: 'Julio',
            8: 'Agosto',
            9: 'Septiembre',
            10: 'Octubre',
            11: 'Noviembre',
            12: 'Diciembre'
        }
        
        return month_dict.get(_month_number)

    @classmethod
    def get_date_now(cls, ):
        return str(datetime.now())

    @classmethod
    def get_operator_dict(cls):
        return {
            "contains": FilterOperator.CONTAINS,
            "equals": FilterOperator.EQUALS,
            # "isNot": FilterOperator.NOTEQUAL,
            # "startsWith": FilterOperator.STARTSWITH,
            # "endsWith": FilterOperator.ENDSWITH,
            # "isEmpty": FilterOperator.ISEMPTY,
            # "isNotEmpty": FilterOperator.NOTEMPTY,
            # "in": FilterOperator.IN,
            # "not_in": FilterOperator.NOT_IN,
            # "=": FilterOperator.EQUALS,
            # "!=": FilterOperator.NOTEQUAL,
            # ">": FilterOperator.GRTHAN,
            # ">=": FilterOperator.GREQTHAN,
            # "<": FilterOperator.LRTHAN,
            # "<=": FilterOperator.LREQTHAN,
            # "is": FilterOperator.IS
        }
    
    @classmethod
    def check_filters(
        cls,
        _filter_column: str,
        _filter_operator: str, 
        _filter_value: str,
        _columns
    ):
        if not _filter_column:
            return False
        cls.check_filter_column(_filter_column, _columns)
        error_msg = f"Para poder hacer el filtro en la columna '{_filter_column}', "

        if not _filter_operator:
            error_msg = f"{error_msg}se necesita especificar un operador de filtro."
            raise BusinessError(error_msg)
        
        
        cls.check_operator(_filter_operator)
        
        if not _filter_value:
            error_msg = f"{error_msg}se necesita proporcionar un valor para aplicar el filtro."
            raise BusinessError(error_msg)

        return True
    
    @classmethod
    def check_operator(
        cls,
        _filter_operator
    ):
        operators_dict = cls.get_operator_dict()
        list_operator_string = operators_dict.keys()
        if _filter_operator not in list_operator_string:
            raise BusinessError(
                f"filter_operator: {_filter_operator} no disponible "
                f"filter_operator disponibles: '{','.join(list_operator_string)}'"
            )

        return True
    
    @classmethod
    def check_filter_column(
        cls,
        _filter_column: str,
        _list_columns_filter: list
    ):
        if _filter_column not in _list_columns_filter:
            raise BusinessError(
                f"filterColumn: {_filter_column} not valid "
                f"filterColumn available: {','.join(_list_columns_filter)}"
            )
        return True

    @classmethod
    def check_sort_type(
        cls,
        _sort_type
    ):
        if _sort_type == 'ASC' or _sort_type == 'DESC':
            return True
        raise BusinessError(f"The Sort Type: {_sort_type} is not valid")
# helpers
from libs.helpers.tools import Tools

# filters
from libs.filters.filters_base import FilterField
from libs.filters.filters_base import FilterOperator

# errors
from libs.errors.business_error import BusinessError
from libs.errors.source_error import NoRecordFoundError

# dao
from dao.product_dao import ProductDao

# models
from models.product_model import ProductModel

# schemas
from schemas.product_schema import ProductSchema


class ProductBsn(object):

    def __init__(
        self,
        _src_mysql=None
    ) -> None:
        self.dao = ProductDao(_src_mysql) if _src_mysql else None
        self.columns = ProductModel.get_columns()
    
    def check_product_key(self, _product_key):
        product_model = ProductModel()
        product_model.product_key = _product_key
        try:
            model_found = self.dao.get_product_dao(product_model)
            return model_found
        except NoRecordFoundError:
            False

    def create_product_bsn(self, _product_schema: ProductSchema):
        if self.check_product_key(_product_schema.product_key):
            error_msg = f"La clave : {_product_schema.product_key} ya existe"
            raise BusinessError(error_msg)

        product_model = ProductModel()
        product_model.product_key = _product_schema.product_key
        product_model.product_description = _product_schema.product_description
        product_model.unit_of_measure = _product_schema.unit_of_measure
        product_model.stock = _product_schema.stock
        
        model = self.dao.insert_product_dao(product_model)
        
        return model

    def get_product_by_id(self, _id: int):
        product_model = ProductModel()
        product_model.id = _id
        try:
            model_found = self.dao.get_product_dao(product_model)
            return model_found
        except NoRecordFoundError:
            error_msg = f"No existe producto: {_id} "
            raise BusinessError(error_msg)
    
    def delete_product_by_id(self, _id: int):
        try:
            product_model = ProductModel()
            product_model.id = _id
            self.dao.delete_product_dao(product_model)
            return True
        except Exception:
            return False
        
    def update_product_bsn(self, _id: int):
        product_model_found = self.check_product_key()
        product_model_update = self.get_product_by_id(_id)

        if product_model_found and product_model_update.id !=  product_model_found.id \
            and  self.data.product_key == product_model_found.product_key:
            error_msg = f"La clave: {self.data.product_key} ya existe"
            raise BusinessError(error_msg)

        
        product_model_update.product_key = self.data.product_key
        product_model_update.product_description = self.data.product_description
        product_model_update.unit_of_measure = self.data.unit_of_measure
        product_model_update.stock = self.data.stock
        product_model_update.product_location = self.data.product_location
        product_model_update.updated_at = Tools.get_date_now()
        
        self.dao.update_product_dao(product_model_update)
        
        return product_model_update

    def get_prodcut_data(
        self,
        _ordering=None,
        _sorting=None,
        _limit=None,
        _page=None,
        _filter_column=None,
        _filter_operator=None,
        _filter_value=None,
    ):
        product_model = ProductModel()
        filters = []
        if _filter_column:
            filter_operator = Tools.get_operator_dict().get(_filter_operator)
            filters.append(FilterField(_filter_column, filter_operator, _filter_value))
        else:
            filters.append(FilterField("product_key", FilterOperator.NOTEMPTY, None))

        items, next_page, total_records = self.dao.search_products(
            _model=product_model,
            _filters=filters,
            _ordering=_ordering,
            _sorting=_sorting,
            _limit=_limit,
            _page=_page
        )

        return items, next_page, total_records
 
# unittest
from unittest import TestCase
from unittest import mock

# sources
from libs.sources.mysql_source import MySQLSource

# business
from bsn.product_bsn import ProductBsn

# models
from models.product_model import ProductModel

# schemas
from schemas.product_schema import ProductSchema

# settings
from settings import MYSQL_CREDENTIAL

class Mock():

    @classmethod
    def product_schema_dummy(cls):
        product_schema = ProductSchema(
            product_key = "enchiladas verdes",
            product_description = "enchiladas verdes",
            unit_of_measure = "ORDEN",
            unit_price = 10.99,
            id_image = "image_id",
            stock = 100,
        )

        return product_schema


class CreateProductBsnTest(TestCase):

    @mock.patch.object(
        ProductBsn,
        'create_product_bsn',
        return_value=ProductModel()
    )
    def test_given_datadict_when_createproduct_then_returnproductmodel(
        self,
        _mock_create_product_bsn,
    ) -> None:
        # src
        src_mysql = MySQLSource(MYSQL_CREDENTIAL)

        # bsn
        bsn_auth = ProductBsn(_src_mysql=src_mysql)
        
        product_schema = Mock.product_schema_dummy()
        product_model = bsn_auth.create_product_bsn(product_schema)

        if src_mysql:
            src_mysql.close_connection()

        # validation
        validation_result = isinstance(product_model, ProductModel)
        self.assertTrue(validation_result, True)

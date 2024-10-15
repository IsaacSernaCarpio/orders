# unittest
from unittest import TestCase
from unittest import mock

# sources
from libs.sources.mysql_source import MySQLSource

# dao
from dao.product_dao import ProductDao

# models
from models.product_model import ProductModel

# settings
from settings import MYSQL_CREDENTIAL

class Mock():

    @classmethod
    def tools_dummy(cls,):
        return None


class InsertProductDaoTest(TestCase):

    @mock.patch.object(
        ProductDao,
        'insert_product_dao',
        return_value=ProductModel()
    )
    def test_given_productmodel_when_isexistdata_then_returntrue(
        self,
        _mock_insert_product_dao,
    ) -> None:
        # src
        src_mysql = MySQLSource(MYSQL_CREDENTIAL)

        # instance
        dao_product = ProductDao(src_mysql)

        # model
        product_model = ProductModel()
        product_model.product_key = 'test_03'
        product_model.product_description = 'test description'
        product_model.unit_of_measure = 'PIEZA'
        # insert dsata
        new_product_model = dao_product.insert_product_dao(product_model)
        # validation
        validation_result = isinstance(new_product_model, ProductModel)
        self.assertTrue(validation_result, True)

        if src_mysql:
            src_mysql.close_connection()


class UpdateProductDaoTest(TestCase):
    @mock.patch.object(
        ProductDao,
        'get_product_dao',
        return_value=ProductModel()
    )
    @mock.patch.object(
        ProductDao,
        'update_product_dao',
        return_value=True
    )
    def test_given_productmodel_when_isexistdataupdate_then_returntrue(
        self,
        _mock_get_product_dao,
        _mock_update_product_dao
    ) -> None:
        # src
        src_mysql = MySQLSource(MYSQL_CREDENTIAL)

        # instance
        dao_product = ProductDao(src_mysql)

        # model
        product_model = ProductModel()
        product_model.id = 1

        # get model
        model_found = dao_product.get_product_dao(product_model)

        # set data
        model_found.product_key = 'test_0001'
        model_found.product_description = 'test description update'

        # update
        result = dao_product.update_product_dao(model_found)
        self.assertTrue(result, True)

        if src_mysql:
            src_mysql.close_connection()

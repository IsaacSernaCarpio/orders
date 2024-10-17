# sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import BOOLEAN
from sqlalchemy import DECIMAL
from sqlalchemy.orm import validates

# datetime
from datetime import datetime

# source
from libs.sources.mysql_declarative import Base

# libs - models
from libs.models.base_mysql import MySQLModel
from libs.models.base_mysql import MySQLModelCollection


class ProductModel(Base, MySQLModel):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_key = Column(String)
    product_description = Column(String)
    unit_of_measure = Column(String)
    unit_price = Column(DECIMAL, default=0.0)
    id_image = Column(String)
    stock = Column(Integer, default=0)
    product_active = Column(BOOLEAN, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        value = f"ProductModel: {self.get_dict()}"
        return value

    @validates('product_key', 'product_description', 'unit_of_measure')
    def convert_to_uppercase(self, _, value):
        if value is not None:
            return value.upper()
        return value

    @classmethod
    def get_columns(cls):
        return cls.__table__.columns.keys()


class ProductCollection(MySQLModelCollection):
    __model__ = ProductModel

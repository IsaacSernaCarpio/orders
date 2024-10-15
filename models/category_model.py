# sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import validates

# datetime
from datetime import datetime

# source
from libs.sources.mysql_declarative import Base

# libs - models
from libs.models.base_mysql import MySQLModel
from libs.models.base_mysql import MySQLModelCollection

class CategoryModel(Base, MySQLModel):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_description = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        value = f"CategoryModel: {self.get_dict()}"
        return value

    @validates('category_description')
    def convert_to_uppercase(self, value):
        if value is not None:
            return value.upper()
        return value

    @classmethod
    def get_columns(cls):
        return cls.__table__.columns.keys()

class CategoryCollection(MySQLModelCollection):
    __model__ = CategoryModel

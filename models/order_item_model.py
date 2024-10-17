# sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates

# datetime
from datetime import datetime

# source
from libs.sources.mysql_declarative import Base

# libs - models
from libs.models.base_mysql import MySQLModel
from libs.models.base_mysql import MySQLModelCollection


class OrderItemModel(Base, MySQLModel):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    notes = Column(String)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # FK
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))

    def __repr__(self):
        value = f"OrderItemModel: {self.get_dict()}"
        return value

    @validates('notes')
    def convert_to_uppercase(self, value):
        if value is not None:
            return value.upper()
        return value

    @classmethod
    def get_columns(cls):
        return cls.__table__.columns.keys()


class OrderItemCollection(MySQLModelCollection):
    __model__ = OrderItemModel

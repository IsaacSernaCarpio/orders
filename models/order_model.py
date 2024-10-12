# sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy import String
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship

# datetime
from datetime import datetime

# source
from libs.sources.mysql_declarative import Base

# libs - models
from libs.models.base_mysql import MySQLModel
from libs.models.base_mysql import MySQLModelCollection


class OrderModel(Base, MySQLModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String)
    order_type = Column(String)
    order_status = Column(String)
    waiter_id = Column(Integer)
    table_id = Column(Integer)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # join
    order_item = relationship("OrderItems", back_populates="order_items")

    def __repr__(self):
        value = f"OrderModel: {self.get_dict()}"
        return value
    
    @validates('order_status')
    def convert_to_uppercase(self, key, value):
        if value is not None:
            return value.upper()
        return value
    
    @classmethod
    def get_columns(cls):
        return cls.__table__.columns.keys()

class OrderCollection(MySQLModelCollection):
    __model__ = OrderModel

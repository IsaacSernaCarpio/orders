# sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy import BOOLEAN
from sqlalchemy import DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship

# datetime
from datetime import datetime

# source
from libs.sources.mysql_declarative import Base

# libs - models
from libs.models.base_mysql import MySQLModel
from libs.models.base_mysql import MySQLModelCollection

class MenuItemModel(Base, MySQLModel):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    available = Column(BOOLEAN, default=True)
    price = Column(DECIMAL, default=0.0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # fk
    product_id = Column(Integer, ForeignKey("product.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

    # join
    product = relationship("Product", back_populates="products")
    category = relationship("Category", back_populates="categories")

    def __repr__(self):
        value = f"MenuItemModel: {self.get_dict()}"
        return value
    
    @classmethod
    def get_columns(cls):
        return cls.__table__.columns.keys()

class MenuItemModelCollection(MySQLModelCollection):
    __model__ = MenuItemModel
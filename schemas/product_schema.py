# pydantic
from pydantic import BaseModel
from pydantic import Field

# decimal
from decimal import Decimal

# typing
from typing import Optional

class ProductSchema(BaseModel):

    id: Optional[int]
    product_key : str = Field(
        description="Identificador de producto / clave",
        example="PRO-001"
    )
    product_description : str = Field(
        description="Descripción de producto",
        example="Suero 500ml"
    )
    unit_of_measure : str = Field(
        description="Unidad de medida",
        example="PIEZA"
    )
    unit_price : Decimal = Field(
        description="Precio unitario",
        example=10.50
    )
    id_image: Optional[str] = Field(None, max_length=50)
    stock : int = Field(
        description="Cantidad existente",
        example=123
    )

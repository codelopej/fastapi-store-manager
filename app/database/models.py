import uuid
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Relationship
from app.schemas import Address, ImageVariants
from app.database.decorators import ModelJsonMapper


class ProductWarehouseLink(SQLModel, table=True):
    __tablename__ = "products_warehouses_link"
    product_id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, foreign_key="products.id", primary_key=True
    )
    warehouse_id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, foreign_key="warehouses.id", primary_key=True
    )
    stock: int


class Warehouse(SQLModel, table=True):
    __tablename__ = "warehouses"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str
    address: Optional[Address] = Field(
        sa_column=Column(ModelJsonMapper(Address), nullable=True)
    )
    phone: Optional[str]
    products: list["Product"] = Relationship(
        back_populates="warehouses", link_model=ProductWarehouseLink
    )


class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str
    description: Optional[str] = None
    current_price: float
    image: Optional[ImageVariants] = Field(
        sa_column=Column(ModelJsonMapper(ImageVariants), nullable=True)
    )
    warehouses: list["Warehouse"] = Relationship(
        back_populates="products", link_model=ProductWarehouseLink
    )


class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str
    description: Optional[str] = None

from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class Address(BaseModel):
    address_1: str
    address_2: Optional[str] = None
    city: str
    state: str
    zip_code: Optional[str] = None
    country: str


class ImageVariants(BaseModel):
    small: Optional[str] = None
    medium: Optional[str] = None
    large: Optional[str] = None
    original: Optional[str] = None


class AddProductsBody(BaseModel):
    products_ids: list[str]


class ResourceRemove(BaseModel):
    id: UUID


class CategoryMutate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryQuery(CategoryMutate):
    id: UUID


class WarehouseMutate(BaseModel):
    name: str
    address: Optional[Address] = None
    phone: Optional[str] = None


class WarehouseQuery(WarehouseMutate):
    id: UUID


class ProductMutate(BaseModel):
    name: str
    description: Optional[str] = None
    current_price: float
    image: Optional[ImageVariants] = None


class ProductQuery(ProductMutate):
    id: UUID


class ProductWarehouseLinkMutateQuery(BaseModel):
    product_id: UUID
    warehouse_id: UUID
    stock: int

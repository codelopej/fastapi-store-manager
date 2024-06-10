from fastapi import APIRouter, HTTPException, Depends
import random
from sqlmodel import Session, select
from app.api.deps import get_session
from app.database.models import Warehouse, Product, ProductWarehouseLink
from app.schemas import (
    ResourceRemove,
    WarehouseMutate,
    WarehouseQuery,
    ProductWarehouseLinkMutateQuery,
    ProductQuery,
    AddProductsBody,
)

router = APIRouter()


@router.get("/", response_model=list[WarehouseQuery])
async def read_warehouses(session: Session = Depends(get_session)):
    return session.exec(select(Warehouse)).all()


@router.get("/{warehouse_id}", response_model=WarehouseQuery)
async def read_warehouse(warehouse_id: str, session: Session = Depends(get_session)):
    with session:
        warehouse = session.get(Warehouse, warehouse_id)
        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        return warehouse


@router.post("/", response_model=WarehouseQuery)
async def create_warehouse(
    warehouse_create: WarehouseMutate, session: Session = Depends(get_session)
):
    warehouse = Warehouse.model_validate(warehouse_create)

    with session:
        exist = bool(
            session.exec(
                select(Warehouse).where(Warehouse.name == warehouse.name)
            ).first()
        )

        if exist:
            raise HTTPException(status_code=400, detail="Warehouse already exists")

        session.add(warehouse)
        session.commit()
        session.refresh(warehouse)
    return warehouse


@router.put("/{warehouse_id}", response_model=WarehouseQuery)
async def update_warehouse(
    warehouse_id: str,
    warehouse_update: WarehouseMutate,
    session: Session = Depends(get_session),
):
    with session:
        warehouse = session.get(Warehouse, warehouse_id)
        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        warehouse_data = warehouse_update.model_dump(exclude_unset=True)
        warehouse.sqlmodel_update(warehouse_data)
        session.add(warehouse)
        session.commit()
        session.refresh(warehouse)
    return warehouse


@router.delete("/{warehouse_id}", response_model=ResourceRemove)
async def delete_warehouse(warehouse_id: str, session: Session = Depends(get_session)):
    with session:
        warehouse = session.get(Warehouse, warehouse_id)
        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        session.delete(warehouse)
        session.commit()
    return {"id": warehouse_id}


@router.get("/{warehouse_id}/products", response_model=list[ProductQuery])
async def read_warehouse_products(
    warehouse_id: str, session: Session = Depends(get_session)
):
    with session:
        warehouse = session.get(Warehouse, warehouse_id)
        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        return warehouse.products


@router.post(
    "/{warehouse_id}/products", response_model=list[ProductWarehouseLinkMutateQuery]
)
async def add_product_to_warehouse(
    warehouse_id: str,
    body: AddProductsBody,
    session: Session = Depends(get_session),
):
    with session:
        warehouse = session.get(Warehouse, warehouse_id)
        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        product_warehouse_link_response = []

        for product_id in body.products_ids:
            product = session.get(Product, product_id)

            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            if product not in warehouse.products:
                product_warehouse_link = ProductWarehouseLink(
                    product_id=product.id,
                    warehouse_id=warehouse.id,
                    stock=random.randint(1, 100),
                )
                session.add(product_warehouse_link)
                session.commit()
                session.refresh(product_warehouse_link)
                product_warehouse_link_response.append(product_warehouse_link)

    return product_warehouse_link_response


@router.delete("/{warehouse_id}/products", response_model=list[ResourceRemove])
async def remove_product_from_warehouse(
    warehouse_id: str, body: AddProductsBody, session: Session = Depends(get_session)
):
    with session:
        warehouse = session.get(Warehouse, warehouse_id)
        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        product_warehouse_link_response = []

        for product_id in body.products_ids:
            product = session.get(Product, product_id)

            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            product_warehouse_link = session.exec(
                select(ProductWarehouseLink).where(
                    ProductWarehouseLink.product_id == product.id,
                    ProductWarehouseLink.warehouse_id == warehouse.id,
                )
            ).first()

            if product_warehouse_link:
                session.delete(product_warehouse_link)
                session.commit()
                product_warehouse_link_response.append(
                    {"id": product_warehouse_link.product_id}
                )

    return product_warehouse_link_response

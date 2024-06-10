from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.api.deps import get_session
from app.database.models import Product
from app.schemas import ResourceRemove, ProductMutate, ProductQuery

router = APIRouter()


@router.get("/", response_model=list[ProductQuery])
async def read_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()


@router.get("/{product_id}", response_model=ProductQuery)
async def read_product(product_id: str, session: Session = Depends(get_session)):
    with session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product


@router.post("/", response_model=ProductQuery)
async def create_product(
    product_create: ProductMutate, session: Session = Depends(get_session)
):
    product = Product.model_validate(product_create)

    with session:
        exist = bool(
            session.exec(select(Product).where(Product.name == product.name)).first()
        )

        if exist:
            raise HTTPException(status_code=400, detail="Product already exists")

        session.add(product)
        session.commit()
        session.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductQuery)
async def update_product(
    product_id: str,
    product_update: ProductMutate,
    session: Session = Depends(get_session),
):
    with session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product_data = product_update.model_dump(exclude_unset=True)
        product.sqlmodel_update(product_data)
        session.add(product)
        session.commit()
        session.refresh(product)
    return product


@router.delete("/{product_id}", response_model=ResourceRemove)
async def delete_product(product_id: str, session: Session = Depends(get_session)):
    with session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        session.delete(product)
        session.commit()
    return {"id": product_id}

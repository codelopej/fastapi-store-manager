from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.api.deps import get_session
from app.database.models import Category
from app.schemas import ResourceRemove, CategoryMutate, CategoryQuery

router = APIRouter()


@router.get("/", response_model=list[CategoryQuery])
async def read_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()


@router.get("/{category_id}", response_model=CategoryQuery)
async def read_category(category_id: str, session: Session = Depends(get_session)):
    with session:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category


@router.post("/", response_model=CategoryQuery)
async def create_category(
    category_create: CategoryMutate, session: Session = Depends(get_session)
):
    category = Category.model_validate(category_create)

    with session:
        exist = bool(
            session.exec(select(Category).where(Category.name == category.name)).first()
        )

        if exist:
            raise HTTPException(status_code=400, detail="Category already exists")

        session.add(category)
        session.commit()
        session.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryQuery)
async def update_category(
    category_id: str,
    category_update: CategoryMutate,
    session: Session = Depends(get_session),
):
    with session:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        category_data = category_update.model_dump(exclude_unset=True)
        category.sqlmodel_update(category_data)
        session.add(category)
        session.commit()
        session.refresh(category)
    return category


@router.delete("/{category_id}", response_model=ResourceRemove)
async def delete_category(category_id: str, session: Session = Depends(get_session)):
    with session:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        session.delete(category)
        session.commit()
    return {"id": category_id}

from fastapi import APIRouter
from .routers.category import router as category_router
from .routers.warehouse import router as warehouse_router
from .routers.product import router as product_router


router = APIRouter()
router.include_router(category_router, prefix="/categories", tags=["categories"])
router.include_router(warehouse_router, prefix="/warehouses", tags=["warehouses"])
router.include_router(product_router, prefix="/products", tags=["products"])

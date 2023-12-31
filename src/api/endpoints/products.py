from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.products import Product
from src.services.products import ProductService

router = APIRouter(
    prefix="/products",
)


@router.post("/add", tags=["AdminZone"])
async def add_product(
    product: Product,
    uow: UOWDep,
):
    product = await ProductService().add_product(uow, product)
    return


@router.get("/", tags=["Main"])
async def get_products(
    uow: UOWDep,
):
    """Get all manufacture's products.

    Args:
        uow (UOWDep): unit of work dependency
    """
    products = await ProductService().get_products(uow)
    return products

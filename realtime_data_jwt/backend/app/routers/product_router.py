from fastapi import APIRouter, Depends

from app.core.auth_dependency import get_current_user
from app.schemes.product_scheme import ProductPublic, ProductUpdate
from app.services.product_service import (
    product_create,
    product_delete,
    product_get,
    product_get_all,
    product_update,
)


# dependencies에 인증 함수를 한 번 넣으면 아래의 모든 API가 보호됩니다.
product_router = APIRouter(
    tags=["Product"],
    dependencies=[Depends(get_current_user)],
)


@product_router.post("/product/create")
def create(product: ProductPublic) -> ProductPublic:
    return product_create(product)


@product_router.get("/product/get/{product_id}")
def get(product_id: int) -> ProductPublic:
    return product_get(product_id)

# @product_router.get("/product/getall")
# def get_all(
#     current_user: str = Depends(get_current_user),
# ) -> list[ProductPublic]:
#     return product_get_all()

@product_router.get("/product/getall")
def get_all() -> list[ProductPublic]:
    return product_get_all()


@product_router.delete("/product/delete/{product_id}")
def delete(product_id: int) -> ProductPublic:
    return product_delete(product_id)


@product_router.put("/product/update/{product_id}")
def update(product_id: int, product: ProductUpdate) -> ProductPublic:
    return product_update(product_id, product)

"""상품 생성·조회·삭제·수정 URL을 정의하는 라우터입니다."""

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
    """요청 Body로 받은 상품을 생성합니다."""

    return product_create(product)


@product_router.get("/product/get/{product_id}")
def get(product_id: int) -> ProductPublic:
    """URL에 포함된 ID로 상품 한 개를 조회합니다."""

    return product_get(product_id)

# @product_router.get("/product/getall")
# def get_all(
#     current_user: str = Depends(get_current_user),
# ) -> list[ProductPublic]:
#     return product_get_all()

@product_router.get("/product/getall")
def get_all() -> list[ProductPublic]:
    """전체 상품 목록을 조회합니다."""

    return product_get_all()


@product_router.delete("/product/delete/{product_id}")
def delete(product_id: int) -> ProductPublic:
    """URL에 포함된 ID의 상품을 삭제합니다."""

    return product_delete(product_id)


@product_router.put("/product/update/{product_id}")
def update(product_id: int, product: ProductUpdate) -> ProductPublic:
    """상품 ID와 수정할 내용을 서비스 함수에 전달합니다."""

    return product_update(product_id, product)

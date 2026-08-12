from fastapi import APIRouter, Depends, status

from app.core.auth_dependency import get_current_user, require_admin
from app.schemes.auth_scheme import CurrentUser
from app.schemes.product_scheme import ProductCreate, ProductPublic, ProductUpdate
from app.services.product_service import (
    product_create,
    product_delete,
    product_get,
    product_get_all,
    product_update,
)


product_router = APIRouter(tags=["Product"])


@product_router.post(
    "/product/create",
    response_model=ProductPublic,
    status_code=status.HTTP_201_CREATED,
)
def create(
    product: ProductCreate,
    current_user: CurrentUser = Depends(require_admin),
):
    """관리자만 상품을 생성할 수 있습니다."""

    return product_create(product, current_user.access_token, current_user.user_id)


@product_router.get("/product/get/{product_id}", response_model=ProductPublic)
def get(
    product_id: int,
    current_user: CurrentUser = Depends(get_current_user),
):
    """로그인한 일반 사용자와 관리자 모두 상품을 조회할 수 있습니다."""

    return product_get(product_id, current_user.access_token)


@product_router.get("/product/getall", response_model=list[ProductPublic])
def get_all(current_user: CurrentUser = Depends(get_current_user)):
    """로그인한 모든 사용자가 전체 상품을 조회할 수 있습니다."""

    return product_get_all(current_user.access_token)


@product_router.delete("/product/delete/{product_id}", response_model=ProductPublic)
def delete(
    product_id: int,
    current_user: CurrentUser = Depends(require_admin),
):
    """관리자만 상품을 삭제할 수 있습니다."""

    return product_delete(product_id, current_user.access_token)


@product_router.put("/product/update/{product_id}", response_model=ProductPublic)
def update(
    product_id: int,
    product: ProductUpdate,
    current_user: CurrentUser = Depends(require_admin),
):
    """관리자만 상품을 수정할 수 있습니다."""

    return product_update(product_id, product, current_user.access_token)

from typing import Any

import httpx
from fastapi import HTTPException

from app.core.db_config import (
    SUPABASE_PUBLISHABLE_KEY,
    SUPABASE_URL,
    check_db_config,
)
from app.schemes.product_scheme import ProductCreate, ProductPublic, ProductUpdate


def request_products(
    method: str,
    access_token: str,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
) -> list[dict]:
    """사용자 Access Token으로 Supabase Data API를 호출하여 RLS를 적용합니다."""

    check_db_config()

    # apikey는 프로젝트를 식별하고 Authorization의 사용자 토큰은 DB 사용자를 식별합니다.
    # service_role을 사용하지 않으므로 products 테이블의 RLS 정책이 항상 실행됩니다.
    headers = {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    try:
        response = httpx.request(
            method,
            f"{SUPABASE_URL}/rest/v1/products",
            params=params,
            json=json,
            headers=headers,
            timeout=10.0,
        )
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=503,
            detail="Supabase Product API에 연결할 수 없습니다.",
        ) from error

    if response.status_code in (401, 403):
        raise HTTPException(
            status_code=403,
            detail="이 Product 작업을 수행할 권한이 없습니다.",
        )

    if response.is_error:
        raise HTTPException(
            status_code=503,
            detail=f"Product DB 처리에 실패했습니다: {response.status_code}",
        )

    if not response.content:
        return []

    return response.json()


def product_create(product: ProductCreate, access_token: str, user_id: str) -> ProductPublic:
    """관리자 토큰으로 상품을 생성합니다. RLS가 관리자 여부를 다시 확인합니다."""

    payload = product.model_dump()
    payload["created_by"] = user_id
    rows = request_products("POST", access_token, json=payload)

    if not rows:
        raise HTTPException(status_code=503, detail="상품 생성 결과가 없습니다.")

    return ProductPublic(**rows[0])


def product_get_all(access_token: str) -> list[ProductPublic]:
    """로그인 사용자 토큰으로 모든 상품을 조회합니다."""

    rows = request_products(
        "GET",
        access_token,
        params={"select": "id,name,price", "order": "id.asc"},
    )
    return [ProductPublic(**row) for row in rows]


def product_get(product_id: int, access_token: str) -> ProductPublic:
    """로그인 사용자 토큰으로 상품 한 개를 조회합니다."""

    rows = request_products(
        "GET",
        access_token,
        params={"select": "id,name,price", "id": f"eq.{product_id}"},
    )

    if not rows:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    return ProductPublic(**rows[0])


def product_delete(product_id: int, access_token: str) -> ProductPublic:
    """관리자 토큰으로 상품을 삭제합니다."""

    rows = request_products(
        "DELETE",
        access_token,
        params={"select": "id,name,price", "id": f"eq.{product_id}"},
    )

    if not rows:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    return ProductPublic(**rows[0])


def product_update(
    product_id: int,
    product: ProductUpdate,
    access_token: str,
) -> ProductPublic:
    """관리자 토큰으로 상품 이름과 가격을 수정합니다."""

    rows = request_products(
        "PATCH",
        access_token,
        params={"select": "id,name,price", "id": f"eq.{product_id}"},
        json=product.model_dump(),
    )

    if not rows:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    return ProductPublic(**rows[0])

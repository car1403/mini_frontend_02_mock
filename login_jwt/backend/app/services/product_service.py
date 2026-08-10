"""DB 없이 상품 CRUD 결과를 만들어 보는 학습용 서비스입니다."""

from app.schemes.product_scheme import ProductPublic
from zoneinfo import ZoneInfo
from datetime import datetime

# 1. 입력
def product_create(product: ProductPublic) -> ProductPublic | None:
    """입력받은 상품을 그대로 반환하여 생성 결과를 흉내 냅니다."""

    # Database 에 입력
    return ProductPublic(
        id = product.id,
        name = product.name,
        price = product.price
    )

# 2. 전체조회
def product_get_all() -> list[ProductPublic]:
    """미리 작성한 상품 여러 개를 목록으로 반환합니다."""

    # 현재는 실제 DB가 없으므로 함수가 실행될 때마다 예제 목록을 만듭니다.
    list = []
    list.append(ProductPublic(
        id = 100,
        name = "바지",
        price = 20000
    ))
    list.append(ProductPublic(
        id = 101,
        name = "바지",
        price = 30000
    ))
    list.append(ProductPublic(
        id = 103,
        name = "바지",
        price = 40000
    ))
    list.append(ProductPublic(
        id = 104,
        name = "바지",
        price = 50000
    ))
    return list 

# 3. 한개조회
def product_get(product_id: str) -> ProductPublic | None:
    """전달받은 ID를 사용하여 예제 상품 한 개를 반환합니다."""

    return ProductPublic(
        id = product_id,
        name = "바지",
        price = 20000
    )

# 4. 삭제
def product_delete(product_id: int) -> ProductPublic | None:
    """실제 삭제 대신 어떤 상품이 삭제됐는지 예제 결과를 반환합니다."""

    return ProductPublic(
        id = product_id,
        name = "삭제된바지",
        price = 20000
    )
# 5. 수정
def product_update(product_id, product: ProductPublic) -> ProductPublic | None:
    """실제 수정 대신 수정되었다는 예제 상품을 반환합니다."""

    return ProductPublic(
        id = product_id,
        name = "수정된바지",
        price = 20000
    )

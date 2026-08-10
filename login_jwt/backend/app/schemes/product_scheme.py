"""상품 API가 주고받는 데이터의 모양을 정의합니다."""

from pydantic import BaseModel, Field

class ProductPublic(BaseModel):
    """상품 전체 정보이며 생성과 조회 응답에 사용합니다."""

    id:int
    name:str
    price:int


class ProductUpdate(BaseModel):
    """상품 수정 시 입력받는 이름과 가격입니다."""

    # 수정할 상품 ID는 요청 Body가 아니라 URL에서 받으므로 여기에는 없습니다.
    name:str
    price:int

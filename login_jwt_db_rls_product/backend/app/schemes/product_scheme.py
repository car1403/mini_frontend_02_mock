from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """관리자가 새 상품을 만들 때 입력하는 데이터입니다."""

    name: str = Field(min_length=1, max_length=100)
    price: int = Field(ge=0)


class ProductUpdate(BaseModel):
    """관리자가 기존 상품을 수정할 때 입력하는 데이터입니다."""

    name: str = Field(min_length=1, max_length=100)
    price: int = Field(ge=0)


class ProductPublic(BaseModel):
    """DB가 만든 ID를 포함하여 프론트엔드에 반환하는 상품입니다."""

    id: int
    name: str
    price: int

from pydantic import BaseModel, Field


class RealDataCreate(BaseModel):
    device_name: str = Field(min_length=1, examples=["sensor-01"])
    temperature: float = Field(examples=[25.5])
    humidity: float = Field(ge=0, le=100, examples=[60])


class RealData(RealDataCreate):
    id: str
    created_at: str


class RealDataResult(RealData):
    """저장 결과와 Redis 실시간 발행 성공 여부입니다."""

    event_published: bool = True

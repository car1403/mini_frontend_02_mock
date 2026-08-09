from pydantic import BaseModel, Field


class RealDataCreate(BaseModel):
    """프론트엔드에서 입력받는 센서 데이터의 모양입니다."""

    device_name: str = Field(min_length=1, examples=["sensor-01"])
    temperature: float = Field(examples=[25.5])
    humidity: float = Field(ge=0, le=100, examples=[60])


class RealData(RealDataCreate):
    """Supabase에 저장된 센서 데이터의 모양입니다."""

    # id와 created_at은 사용자가 입력하지 않고 Supabase가 자동으로 만듭니다.
    id: str
    created_at: str


class RealDataResult(RealData):
    """저장된 데이터에 Redis 전송 결과를 추가한 응답입니다."""

    # True이면 Redis 채널 전송까지 성공했다는 뜻입니다.
    event_published: bool = True

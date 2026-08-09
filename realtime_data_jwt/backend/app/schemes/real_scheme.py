from pydantic import BaseModel, Field


class RealDataCreate(BaseModel):
    device_name: str = Field(min_length=1, examples=["sensor-01"])
    temperature: float = Field(examples=[25.5])
    humidity: float = Field(ge=0, le=100, examples=[60])


class RealData(RealDataCreate):
    id: str
    created_by: str
    created_at: str

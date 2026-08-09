from pydantic import BaseModel


class RealData(BaseModel):
    number: int
    temperature: int
    status: str
    created_at: str

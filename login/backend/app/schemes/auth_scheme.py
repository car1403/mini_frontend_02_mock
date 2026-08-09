# product_scheme.py
from pydantic import BaseModel, Field

class AuthPublic(BaseModel):
    id:str
    name:str  | None = None


class AuthLogin(BaseModel):
    id:str
    pwd:str 
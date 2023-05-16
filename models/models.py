from typing import Optional

from pydantic import BaseModel


class CodeStatus(BaseModel):
    code: str
    status: str


class InvalidCode(CodeStatus):
    pass

class BuyerData(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    buyer_city: Optional[str]
    purchase_source: Optional[str]
    verified_on_utc: Optional[str]


class CodeDetails(BaseModel):
    code: str
    qr_id: str
    status: str
    buyer_data: Optional[BuyerData]


class UserDetails(BaseModel):
    username: str
    name: Optional[str]
    email: Optional[str]
    credit_count: Optional[int]
    subdomain: Optional[str]

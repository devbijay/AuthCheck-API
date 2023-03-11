from typing import Optional

from pydantic import BaseModel


class CodeStatus(BaseModel):
    code: str
    status: str


class BuyerData(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    purchase_source: Optional[str]
    verified_on_utc: Optional[str]


class CodeDetails(BaseModel):
    code: str
    qr_id: str
    status: str
    buyer_data: Optional[BuyerData]

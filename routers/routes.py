from typing import Optional
from fastapi import APIRouter, Header, Security, Depends, HTTPException, status, Query
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

from models.models import CodeStatus, CodeDetails, BuyerData
from services.database import db

load_dotenv()
router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key")


async def auth_required(api_key: Optional[str] = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key is missing in header")

    if user := db.users.find_one({"api": api_key}, {"username": 1}):
        return user.get("username")

    raise HTTPException(status_code=401, detail="Invalid API key")


@router.get("/hello")
async def read_item(user: str = Depends(auth_required)):
    return {"message": "hello World"}


@router.get("/status", response_model=CodeStatus)
async def get_code_status(code: str = Query(description="Code Id or Qr Id", min_length=8),
                          user: str = Depends(auth_required)):
    if result := db.codes.find_one({"owner_name": user, "$or": [{"code": code}, {"_id": code}]},
                                   {"_id": 0, "status": 1}):
        return CodeStatus(code=code, status="used" if result.get("status") else "not_used")
    return CodeStatus(code=code, status="Invalid Code")


@router.get("/details", response_model=CodeDetails)
async def get_code_details(code: str = Query(description="Code Id or Qr Id", min_length=8),
                           user: str = Depends(auth_required)):
    if result := db.codes.find_one({"owner_name": user, "$or": [{"code": code}, {"_id": code}]}):
        buyer_data = BuyerData(name=result.get("buyer_name"),
                               phone=result.get("buyer_phone"),
                               email=result.get("buyer_email"),
                               purchase_source=result.get("purchase_source"),
                               verified_on_utc=str(result.get("verified_on"))
                               )

        return CodeDetails(code=code,
                           qr_id=result.get("_id"),
                           status="used" if result.get("status") else "not_used",
                           buyer_data=buyer_data
                           )

    return CodeStatus(code=code, status="Invalid Code")

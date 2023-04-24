import os
from typing import Optional, Union
from fastapi import APIRouter, Header, Security, Depends, HTTPException, status, Query
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
from redis import Redis
from models.models import CodeStatus, CodeDetails, BuyerData, UserDetails, InvalidCode
from services.database import db


load_dotenv()
router = APIRouter()



api_key_header = APIKeyHeader(name="X-API-Key")

redis = Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASS')
)


async def auth_required(api_key: Optional[str] = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key is missing in header")

    if user := redis.get(api_key):
        return user.decode('utf-8')

    raise HTTPException(status_code=401, detail="Invalid API key")


@router.post("/status", response_model=CodeDetails, responses={404: {"model": InvalidCode}}, tags=["Code Management"])
async def get_code_details(code: str = Query(description="Code Id or Qr Id", min_length=8),
                           user: str = Depends(auth_required)):

    code_filter = {'_id': code} if len(code) == 26 else {'code': code, 'owner_name': user}

    if result := db.unused_codes.find_one(code_filter):
        return CodeDetails(code=code,
                           qr_id=result.get("_id"),
                           status="not_used",
                           buyer_data=""
                           )

    elif result := db.codes.find_one(code_filter):
        return CodeDetails(code=code,
                           qr_id=result.get("_id"),
                           status="used" if result.get("status") else "not_used",
                           buyer_data=BuyerData(name=result.get("buyer_name"),
                                                phone=result.get("buyer_phone"),
                                                email=result.get("buyer_email"),
                                                buyer_city=result.get("b_city"),
                                                purchase_source=result.get("purchase_source"),
                                                verified_on_utc=str(result.get("verified_on"))))

    return InvalidCode(code=code, status="Invalid Code")


@router.post("/userinfo", response_model=UserDetails, tags=["User Management"])
async def get_account_information(user: str = Depends(auth_required)):
    q_res = db.users.find_one({"username": user}, {"role": 0, "activity": 0, "signup_date": 0, "password": 0})
    return UserDetails(
        username=q_res['username'],
        name=q_res['name'],
        email=q_res['email'],
        credit_count=q_res['credit'],
        subdomain=q_res['settings'].get('subdomain')
    )


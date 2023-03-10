from functools import wraps

from fastapi import APIRouter, Header, Security, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
from services.database import db

load_dotenv()
router = APIRouter()

auth_scheme = APIKeyHeader(name="X_API_KEY")


def auth_required(api_key: str = Depends(auth_scheme)):
    if api_key is None:
        return {"message": "Api key is missing in the header"}, 401

    if db.users.find_one({"api": api_key}):
        return True

    return {"message": "Invalid API key"}, 401


@router.get("/hello")
@auth_required
async def read_item(dependencies=[Depends(auth_required)]):
    return {"item_id": "item_id", "source": "route2"}

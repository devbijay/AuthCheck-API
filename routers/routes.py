from functools import wraps

from fastapi import APIRouter, Header
from dotenv import load_dotenv
from services.database import db
load_dotenv()
router = APIRouter()


def auth_required(f):
    @wraps(f)
    def decorated(*args,X_API_KEY: str = Header(None), **kwargs):
        if X_API_KEY is None:
            return {"message": "Api key is missing in the header"}, 401

        if user := db.users.find_one({"api": X_API_KEY}):
            kwargs['username'] = user.get("username")
            return f(*args, **kwargs)

        return {"message": "Invalid API key"}, 401

    return decorated


@router.get("/hello")
@auth_required
async def read_item(item_id: int):
    return {"item_id": item_id, "source": "route2"}

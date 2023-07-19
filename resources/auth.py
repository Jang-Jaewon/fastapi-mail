from fastapi import APIRouter

from managers.user import UserManager

router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201)
async def register(user_data):
    token = await UserManager.register(user_data.dict())
    return {"token": token}
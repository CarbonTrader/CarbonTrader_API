from fastapi import FastAPI, APIRouter
from typing import Union
from typing import List

from app.Model.User import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test":"test"}

@router.get("/{user_id}")
async def get_user(user_id):
    return DUMMY_RESPONSE

@router.put("/")
async def update_user_info(user: User):
    return DUMMY_RESPONSE

@router.delete("/{user_id}")
async def delete_user(user_id):
    return DUMMY_RESPONSE



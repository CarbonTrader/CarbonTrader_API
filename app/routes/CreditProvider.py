from fastapi import FastAPI, APIRouter

from typing import Union
from typing import List

from app.Model.Credit import Credit

router = APIRouter(
    prefix="/credits",
    tags=["Credits"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test":"test"}

@router.get("/{user_id}")
async def get_user_credits(user_id):
    return DUMMY_RESPONSE

@router.get("/{project_id}")
async def get_project_credits(project_id):
    return DUMMY_RESPONSE

@router.get("/{credit_id}")
async def get_credit_info(credit_id):
    return DUMMY_RESPONSE

@router.post("/")
async def create_credit(new_credit: Credit):
    return DUMMY_RESPONSE

@router.put("/")
async def update_credit(updated_credit: Credit):
    return DUMMY_RESPONSE

@router.put("/buy")
async def buy_credit(q: Union[List[str],None]):
    return str(q)

#TODO: Solo usuarios autenticados dueños de esos creditos
@router.put("/sell")
async def sell_credits(q: Union[List[str],None]):
    return str(q)



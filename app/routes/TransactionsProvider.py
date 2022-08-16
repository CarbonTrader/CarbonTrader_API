from fastapi import FastAPI, APIRouter
from typing import Union
from typing import List

from app.Model.Transaction import Transaction

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test":"test"}

@router.get("/")
async def get_global_transactions(trans_id):
    return DUMMY_RESPONSE

@router.get("/{trans_id}")
async def get_transaction(trans_id):
    return DUMMY_RESPONSE

@router.get("/{user_id}")
async def get_user_transactions(user_id):
    return DUMMY_RESPONSE

@router.post("/")
async def create_transaction(transaction: Transaction):
    return transaction


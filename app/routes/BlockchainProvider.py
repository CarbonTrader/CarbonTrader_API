from fastapi import FastAPI, APIRouter, Body
from app.blockchain.Transaction import Transaction
from app.blockchain.Wallet import Wallet
import json

router = APIRouter(
    prefix="/blockchain",
    tags=["blockchain"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test": "test"}


@router.get("/")
async def get_user_credits(transaction_data: dict = Body(...)):
    pass

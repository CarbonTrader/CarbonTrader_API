
from app.Model.Transaction import Transaction
from fastapi import FastAPI, APIRouter, Body
from app.blockchain.Transaction import Transaction
from app.blockchain.Wallet import Wallet
from typing import Union, List

from app.services.TransactionService import TransactionService

router = APIRouter(
    prefix="/transaction",
    tags=["Transactions"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test": "test"}


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
async def create_transaction(transaction_data: dict = Body(...)):
    wallet = Wallet()
    trans = Transaction(transaction_data.get("id"), transaction_data.get("type"),
                        transaction_data.get("serial"), wallet, transaction_data.get("recipient"))
    return TransactionService.create_transaction(trans.__dict__)

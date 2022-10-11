
from app.Model.Transaction import Transaction
from fastapi import FastAPI, APIRouter, Body
from app.blockchain.Transaction import Transaction
from app.blockchain.Wallet import Wallet
from typing import Union, List
import uuid
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

"""
transaction_data = {
    "carbon_trader_serial":"carbon-trader-09-302-00",
    "recipient_email": "mario12@gmail.com",
    "sender_email":"e@example.com"
    "private_key_sender": "-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgyRdwdavTbmfBldZgylzU\nXyYxX5WPe+WAHmQaDkrXiOmhRANCAARawkffg+hxUcor68JsWX7/lW0YNs+rbp3b\nrE9TolBzgi77cVklf6qmTRwKeXUUqSU9FnnMm5mQiurtCimbzu50\n-----END PRIVATE KEY-----\n"
    "public_key_sender: "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEWsJH34PocVHKK+vCbFl+/5VtGDbPq26d\n26xPU6JQc4Iu+3FZJX+qpk0cCnl1FKklPRZ5zJuZkIrq7Qopm87udA==\n-----END PUBLIC KEY-----\n"
}
"""


@router.post("/exchange")
async def exchange_credit(transaction_data: dict = Body(...)):
    transaction_data["type"] = "exchange"
    return TransactionService.build_transaction(transaction_data)


@router.post("/retire")
async def retire_credit(transaction_data: dict = Body(...)):
    transaction_data["type"] = "retire"
    transaction_data["recipient_email"] = "anonimo@gmail.com"
    print(transaction_data)
    return TransactionService.build_transaction(transaction_data)


@router.post("/")
async def create_transaction(transaction_data: dict = Body(...)):
    wallet = Wallet()
    trans = Transaction(transaction_data.get("id"), transaction_data.get("type"),
                        transaction_data.get("serial"), wallet, transaction_data.get("recipient"))
    return TransactionService.create_transaction(trans.__dict__)

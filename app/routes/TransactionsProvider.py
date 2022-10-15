from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
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


@router.get("/all")
async def get_all():
    try:
        response = TransactionService.get_all_transactions()
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)

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

@router.post("/many/exchange")
async def exchange_many_credits(transaction_data:dict = Body(...)):
    print("entra")
    print(transaction_data)
    #transaction_data["type"] = "exchange"
    return True
#TransactionService.build_transaction(transaction_data)


@router.post("/retire")
async def retire_credit(transaction_data: dict = Body(...)):
    transaction_data["type"] = "retire"
    transaction_data["recipient_email"] = "anonimo@gmail.com"
    return TransactionService.build_transaction(transaction_data)


@router.post("/")
async def create_transaction(transaction_data: dict = Body(...)):
    wallet = Wallet()
    trans = Transaction(transaction_data.get("id"), transaction_data.get("type"),
                        transaction_data.get("serial"), wallet, transaction_data.get("recipient"))
    return TransactionService.upload_transaction_to_blockchain(trans.__dict__)

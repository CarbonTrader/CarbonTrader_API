from fastapi import FastAPI, APIRouter, Body
from app.blockchain.Transaction import Transaction
from app.blockchain.Wallet import Wallet
import json
from app.services.BlockchainService import main


router = APIRouter(
    prefix="/blockchain",
    tags=["blockchain"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test": "test"}

transaction_test = {
    "id": "id",
    "timestamp": 1662404005673912600,
    "recipient_address": "recipient",
    "sender_address": "890447ee-004a-4861-b289-17ef7fe1816d",
    "carbon_trader_serial": "serial",
    "transaction_type": "type",
    "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBcMoHMcdSZH4rN9MnqJiaY1/9m0uA3FB\nfnLsjb5pbOR4W2WalwISvN5KMgUomet73ueIEqQmq/Fzpw0kXzEEag==\n-----END PUBLIC KEY-----\n",
    "hash": "26a685f538379e01a6969c3b70269c6a64ec4b1a5086b234352571ef249745e4",
    "signature": [
            94569455730509609095865838898061247101293443266325724040836884706485395646916,
            41685141177766446954308376254462600693323834175649420393960287882615972537065
    ]
}

"""
    {
        id: "id",
        type: "type",
        serial: "serial",
        pk: "pk",
        recipient: "address"
    }
"""

#TODO: validate


@router.get("/")
async def get_user_credits(transaction_data: dict = Body(...)):
    print(transaction_data)
    wallet = Wallet()
    trans = Transaction(transaction_data.get("id"), transaction_data.get("type"),
                        transaction_data.get("serial"), wallet, transaction_data.get("recipient"))
    return main(trans.__dict__)

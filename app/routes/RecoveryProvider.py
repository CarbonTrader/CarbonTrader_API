from fastapi import APIRouter, HTTPException
from app.services.RecoveryService import RecoveryService
from fastapi import APIRouter, Body
from typing import List

router = APIRouter(
    prefix="/recovery",
    tags=["recovery"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test": "test"}


@router.get("/")
async def get_backup_blockchain():
    return RecoveryService.get_blockchain()


@router.put("/")
async def update_backup_blockchain(transaction_data: List[dict] = Body(...)):
    return RecoveryService.update_blockchain(transaction_data)

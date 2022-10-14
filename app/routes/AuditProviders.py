from app.services.AuditService import AuditService
from app.services.TransactionService import TransactionService
from fastapi import APIRouter, HTTPException, Body
from app.services.RecoveryService import RecoveryService
from typing import List
router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def begin_audit(params: dict = Body(...)):
    try:
        auditor = AuditService()
        auditor.begin_audit(params)
    except:
        return {"asd":"asd"}



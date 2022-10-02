from fastapi import APIRouter, HTTPException
from firebase_admin import db
from app.services.ProjectService import ProjectService
from app.Model.Project import Project
from app.services.RecoveryService import RecoveryService

router = APIRouter(
    prefix="/recovery",
    tags=["recovery"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test": "test"}


@router.get("/")
async def get_backup_blockchain():
    return RecoveryService.get_blockchina()


@router.put("/")
async def update_backup_blockchain():
    return DUMMY_RESPONSE

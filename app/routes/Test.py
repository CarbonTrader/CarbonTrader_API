from fastapi import FastAPI, APIRouter
from ..services.BlockService import BlockService

from app.services.TransactionService import TransactionService
from app.services.WalletService import WalletService

router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def test():
    WalletService().test()


@router.get("/2")
def test():
    TransactionService().test()


@router.get("/3")
def test():
    BlockService().test()

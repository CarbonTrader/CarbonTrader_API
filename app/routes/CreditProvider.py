from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from firebase_admin import db
from app.services.CreditService import CreditService
from typing import Union
from typing import List

from app.Model.Credit import Credit

router = APIRouter(
    prefix="/credits",
    tags=["Credits"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test": "test"}


@router.get("/provider_email/{serial}")
async def get_provider_email(serial: str):
    try:
        response = CreditService.get_provider_email(serial)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=400)
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.get("/project/{credit_serial}")
async def get_project_by_serial(credit_serial: str):
    try:
        response = CreditService.get_project_by_serial(credit_serial)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.get("/{project_id}")
async def get_project_credits(project_id):
    return DUMMY_RESPONSE


@router.get("/{credit_id}")
async def get_credit_info(credit_id):
    return DUMMY_RESPONSE


@router.post("/")
async def create_credit(new_credit: Credit):
    return DUMMY_RESPONSE


@router.put("/")
async def update_credit(updated_credit: Credit):
    return DUMMY_RESPONSE


@router.put("/buy")
async def buy_credit(q: Union[List[str], None]):
    return str(q)


# TODO: Solo usuarios autenticados dueños de esos creditos
@router.put("/sell")
async def sell_credits(q: Union[List[str], None]):
    return str(q)

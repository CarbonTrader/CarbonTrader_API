from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.Model.User import User
from ..services.AuthService import AuthService
from ..services.UserService import UserService
from fastapi import FastAPI, APIRouter, Body

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test": "test"}


@router.get("/{email}")
async def get_user(email):
    try:
        response = AuthService.get_user(email)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.get("/credits/{email}")
async def get_user(email):
    try:
        response = UserService.get_trader_credits(email)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.get("/transactions/{email}")
async def get_transactions(email):
    try:
        response = UserService.get_transactions(email)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.get("/keys/{email}")
async def get_user_keys(email):
    try:
        response = UserService.get_keys(email)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.post("/sale_credit")
async def get_transactions(transaction_data: dict = Body(...)):
    try:
        response = UserService.sale_credit(transaction_data['email'], transaction_data['serial'],
                                           transaction_data['project_id'])
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content="", status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.put("/")
async def update_user_info(user: User):
    try:
        response = UserService.update_user(user)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.delete("/{user_id}")
async def delete_user(user_id):
    return DUMMY_RESPONSE

from fastapi import APIRouter, HTTPException, Body
from fastapi import Request
from fastapi.responses import JSONResponse

from ..Model.SignUpRequest import SignUpRequest
from ..services.AuthService import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}, 200: {"description": "Successfully operation"}},
)


# signup endpoint
@router.post("/signup", include_in_schema=False)
async def signup(request: SignUpRequest):
    try:
        response = AuthService.sign_up(request)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=400)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


# login endpoint
@router.post("/login", include_in_schema=False)
async def login(request: Request):
    try:
        response = await AuthService.login(request)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=400)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.delete("/delete/{user_email}", responses={204: {"model": None}})
async def remove_user_account(user_email: str):
    await AuthService.remove_trader_account(user_email)

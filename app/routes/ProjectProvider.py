from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from firebase_admin import db
from app.services.ProjectService import ProjectService
from app.Model.CreateProjectRequest import CreateProjectRequest
from app.Model.Project import Project

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/all")
async def get_projects():
    try:
        response = ProjectService.get_all_projects()
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=400)
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.post("/create", status_code=201, include_in_schema=False)
async def create_project(request: CreateProjectRequest):
    try:
        response = ProjectService.create_project(request.auth_token, request.new_project, request.email)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=400)
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.get("/provider_email/{project_id}")
async def get_provider_email(project_id: str):
    try:
        response = ProjectService.get_provider_email(project_id)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=400)
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.get("/onSaleCredits/{project_id}")
async def get_credits(project_id: str):
    try:
        response = ProjectService.get_on_sale_credits(project_id)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.get("/onSaleCredits/provider/{project_id}")
async def get_credits(project_id: str):
    try:
        response = ProjectService.get_cp_on_sale_credits(project_id)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.post("/{auth_token}", status_code=201, response_model=Project)
async def create_project(auth_token: str, new_project: Project):
    if not ProjectService.create_project(auth_token, new_project):
        raise HTTPException(status_code=404, detail="Invalid authToken.")
    return new_project


@router.get("/import")
async def import_projects():
    try:
        response = ProjectService.create_list_projects()
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=400)
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)


@router.get("/credit_provider/{project_id}")
async def get_credit_provider(project_id: str):
    try:
        response = ProjectService.get_credit_provider(project_id)
        if isinstance(response, Exception):
            return HTTPException(detail={'error': str(response)}, status_code=404)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return HTTPException(detail={'error': str(e)}, status_code=500)

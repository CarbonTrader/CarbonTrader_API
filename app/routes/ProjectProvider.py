from fastapi import APIRouter, HTTPException
from firebase_admin import db
from app.services.ProjectService import ProjectService
from app.Model.Project import Project

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test": "test"}


@router.get("/")
async def get_projects():
    return DUMMY_RESPONSE


@router.get("/{project_id}")
async def get_project():
    return DUMMY_RESPONSE


@router.post("/{auth_token}", status_code=201, response_model=Project)
async def create_project(auth_token: str, new_project: Project):
    if not ProjectService.create_project(auth_token,new_project):
        raise HTTPException(status_code=404, detail="Invalid authToken.")
    return new_project


@router.put("/{auth_token}")
async def update_project(auth_token, updated_project: Project):
    return DUMMY_RESPONSE

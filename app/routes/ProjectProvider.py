from fastapi import FastAPI, APIRouter

from app.Model.Project import Project

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    responses={404: {"description": "Not found"}},
)

DUMMY_RESPONSE = {"test":"test"}

@router.get("/")
async def get_projects():
    return DUMMY_RESPONSE

@router.get("/{project_id}")
async def get_project():
    return DUMMY_RESPONSE

@router.post("/{auth_token}")
async def create_project(auth_token,new_project: Project):
    return DUMMY_RESPONSE

@router.put("/{auth_token}")
async def update_project(auth_token, updated_project: Project):
    return DUMMY_RESPONSE

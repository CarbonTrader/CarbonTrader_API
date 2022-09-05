from app.Model import Project
from firebase_admin import db
class ProjectService:
    @staticmethod
    def create_project(auth_token: str, new_project: Project):
        projects_ref = db.reference("/projects")
        credit_providers_ref = db.reference("credit-provider/" + auth_token)
        credit_provider = credit_providers_ref.get()
        if not credit_provider:
            return None

        credit_providers_projects_ref = db.reference("credit-provider/" + auth_token + "/projects")
        projects_ref.push(new_project.dict())
        credit_providers_projects_ref.push(new_project.dict())
        return new_project
import requests

from app.Model.Project import Project
from app.config.firebaseConfig import db


# from firebase_admin import db

def generate_credit_id(email, token, project, credit):
    return email[:2].upper() + '_' + token[:2].upper() + '_' + project['id'].upper() + '_' \
           + project['project_verifier'][:1].upper() + project['project_verifier'][-1].upper() + '_' \
           + project['evaluation_criteria'][:1].upper() + project['evaluation_criteria'][-1].upper() + '_' \
           + project['quantification_methodology'][0][:1].upper() \
           + project['quantification_methodology'][0][-1].upper() + '_' \
           + credit['credit_provider_serial'][-4:]


def build_project_from_imported_project(imported_project, n):
    img = [imported_project['image']]
    qm = imported_project['Quantification_methodology'].split(':')
    new_project = Project(id=str(n), name=imported_project['project'], description=str(imported_project['description']),
                          images=img, project_verifier=imported_project['verifier'], sector=imported_project['Sector'],
                          evaluation_criteria=imported_project['evaluation_criteria'], quantification_methodology=qm,
                          credits=[])

    db.collection('CreditProvider').document("Provider@example.com").collection('GreenProjects').document(str(n)).set(
        new_project.dict())


class ProjectService:

    @staticmethod
    def create_project(auth_token: str, new_project: Project, email: str):
        user = db.collection('CreditProvider').document(email).get()
        project = new_project.dict()
        if not user.exists:
            raise Exception('Not found user')

        user = user.to_dict()
        if not user['uuid'] == auth_token:
            raise Exception('El token de autenticación no es correcto')

        for credit in project['credits']:
            credit['carbontrader_serial'] = generate_credit_id(email, auth_token, project, credit)
            user['wallet']['owned_credits'].append(credit['carbontrader_serial'])

        db.collection('CreditProvider').document(email).set(user)

        db.collection('CreditProvider').document(email) \
            .collection('GreenProjects').document(new_project.id).set(project)

        return project

    @staticmethod
    def get_on_sale_credits(project_id: str):
        result_credits = []

        users = db.collection('CreditProvider').stream()
        for user in users:
            user = user.to_dict()
            email = user['email']
            projects = db.collection('CreditProvider').document(email).collection('GreenProjects').stream()
            for project in projects:
                project = project.to_dict()
                if str(project['id']) == project_id:
                    cp = db.collection('CreditProvider').document(email).get()
                    cp = cp.to_dict()
                    wallet_credits = cp['wallet']['owned_credits']
                    credits = project['credits']

                    for credit in credits:
                        if credit['carbontrader_serial'] in wallet_credits:
                            result_credits.append(credit)
        object = {
            "serial": "",
            "project_id": "",
            "owner": "",
            "retire_date": "",
            "price": ""
        }
        onSale_credits = db.collection("Seriales_En_Venta").stream()
        for c in onSale_credits:
            c = c.to_dict()
            if (c['project_id'] == project_id):
                object['serial'] = c['serial']
                object['project_id'] = c['project_id']
                object['owner']= c['owner']
                result_credits.append(object)
        return result_credits

    @staticmethod
    def get_cp_on_sale_credits(project_id: str):
        result1_credits = []
        result2_credits = []
        users = db.collection('CreditProvider').stream()
        for user in users:
            user = user.to_dict()
            email = user['email']
            projects = db.collection('CreditProvider').document(email).collection('GreenProjects').stream()
            for project in projects:
                project = project.to_dict()
                if str(project['id']) == project_id:
                    result1_credits.extend(user['wallet']['owned_credits'])
                    result2_credits.extend(project['credits'])
                    result2_credits = list(map(lambda credit: credit['carbontrader_serial'], result2_credits))

        return list(set(result1_credits).intersection(result2_credits))

    @staticmethod
    def get_all_projects():
        p = []
        cp = db.collection('CreditProvider').stream()
        for user in cp:
            user = user.to_dict()
            email = user['email']
            projects = db.collection('CreditProvider').document(email).collection('GreenProjects').stream()
            for project in projects:
                project = project.to_dict()
                p.append(project)

        return p

    @staticmethod
    def get_provider_email(project_id):
        credit_providers = db.collection('CreditProvider').stream()
        for provider in credit_providers:
            provider = provider.to_dict()
            projects = db.collection('CreditProvider').document(provider['email']).collection('GreenProjects').stream()
            for project in projects:
                project = project.to_dict()
                if project['id'] == project_id:
                    return provider['email']
        return None

    @staticmethod
    def create_list_projects():
        n = 0
        url = 'https://api-credit-provider.herokuapp.com/'
        response = requests.get(url)
        imported_projects = response.json()
        for project in imported_projects:
            build_project_from_imported_project(project, n)
            n = n + 1
        return ''

    @staticmethod
    def get_credit_provider(project_id: str):
        users = db.collection('CreditProvider').stream()
        for user in users:
            user = user.to_dict()
            email = user['email']
            projects = db.collection('CreditProvider').document(email).collection('GreenProjects').stream()
            for project in projects:
                project = project.to_dict()
                print(project['id'])
                if str(project['id']) == project_id:
                    return email
        raise Exception('Not found project')

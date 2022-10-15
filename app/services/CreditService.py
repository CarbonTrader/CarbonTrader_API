from app.Model import Credit
from app.config.firebaseConfig import db


# TODO: Logic of the credits
class CreditService:
    @staticmethod
    def get_provider_email(serial):
        credit_providers = db.collection('CreditProvider').stream()
        for provider in credit_providers:
            provider = provider.to_dict()
            projects = db.collection('CreditProvider').document(provider['email']).collection('GreenProjects').stream()
            for project in projects:
                project = project.to_dict()
                project_credits = project['credits']
                for credit in project_credits:
                    if credit['carbontrader_serial'] == serial:
                        return provider['email']
        return None

    @staticmethod
    def get_project_by_serial(carbontrader_serial: str):
        users = db.collection('CreditProvider').stream()
        for user in users:
            user = user.to_dict()
            email = user['email']
            projects = db.collection('CreditProvider').document(email).collection('GreenProjects').stream()
            for project in projects:
                project = project.to_dict()
                project_credits = project['credits']
                for credit in project_credits:
                    if credit['carbontrader_serial'] == carbontrader_serial:
                        return credit
        raise Exception('Not found project')

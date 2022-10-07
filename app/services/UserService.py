from app.config.firebaseConfig import db


class UserService:

    @staticmethod
    def get_user(user_email):
        response = {"collection": "", "response": ""}
        credit_provider_user = db.collection(
            'CreditProvider').document(user_email).get()
        if credit_provider_user.exists:
            response["collection"] = "CreditProvider"
            response["response"] = credit_provider_user.to_dict()
            return response

        investor_user = db.collection('Trader').document(user_email).get()
        if investor_user.exists:
            response["collection"] = "Trader"
            response["response"] = investor_user.to_dict()
            return response

        auditor_user = db.collection('Auditors').document(user_email).get()
        if auditor_user.exists:
            response["collection"] = "Auditor"
            response["response"] = auditor_user.to_dict()
            return response
        return None

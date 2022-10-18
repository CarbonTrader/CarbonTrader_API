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

    @staticmethod
    def get_trader_credits(user_email):
        user_credits = []
        user = db.collection('Trader').document(user_email).get()
        if not user.exists:
            raise Exception('Not found trader')
        user = user.to_dict()
        trader_credits = user['wallet']['owned_credits']
        for aux in trader_credits:
            user_credits.append(aux)
        #   onSale_credits = db.collection('Seriales_En_Venta').stream()
        #   for c in onSale_credits:
        #       c = c.to_dict()
        #       if c['owner'] == user_email:
        #           user_credits.append(c['serial'])

        return user_credits

    @staticmethod
    def get_transactions(user_email):
        user_transactions = []
        user = db.collection('Trader').document(user_email).get()
        if not user.exists:
            raise Exception('Not found trader')
        transactions = db.collection('Trader').document(user_email).collection('Transactions').stream()
        for t in transactions:
            t = t.to_dict()
            user_transactions.append(t)

        return user_transactions

    @staticmethod
    def sale_credit(user_email, serial, project_id):
        user = db.collection('Trader').document(user_email).get()
        if not user.exists:
            raise Exception('Not found trader')

        user = user.to_dict()
        user_credits = user['wallet']['owned_credits']

        # user_credits.remove(serial)

        # user['wallet']['owned_credits'] = user_credits
        # db.collection('Trader').document(user_email).set(user)

        sale_credit = {
            'owner': user_email,
            'project_id': project_id,
            'serial': serial
        }

        db.collection('Seriales_En_Venta').document(serial).set(sale_credit)

    @staticmethod
    def get_keys(email):
        obj = {
            'pub_key': '',
            'priv_key': ''
        }
        credit_provider_user = db.collection(
            'CreditProvider').document(email).get()
        if credit_provider_user.exists:
            user = credit_provider_user.to_dict()
            obj['pub_key'] = user['wallet']['public_key']
            obj['priv_key'] = user['wallet']['private_key']
            return obj

        investor_user = db.collection('Trader').document(email).get()
        if investor_user.exists:
            user = investor_user.to_dict()
            obj['pub_key'] = user['wallet']['public_key']
            obj['priv_key'] = user['wallet']['private_key']
            return obj

    @staticmethod
    def update_user(new_user):
        found_user = db.collection('Trader').document(new_user['email']).get()
        if not found_user.exists:
            raise Exception('Not found user')

        found_user = found_user.to_dict()

        found_user['name'] = new_user['name']
        db.collection('Trader').document(found_user['email']).set(found_user)
        return found_user

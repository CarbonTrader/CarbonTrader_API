import json
import uuid

import pyrebase
from firebase_admin import auth

from app.Model.SignUpRequest import SignUpRequest
from ..config.firebaseConfig import db
from app.blockchain.Wallet import Wallet

pb = pyrebase.initialize_app(json.load(open('app/secrets/firebase_config.json')))


def add_user(name, email, role, collection):
    user_data = {
        'name': name,
        'email': email,
        'role': role,
    }
    user_uuid = uuid.uuid4() if role != 'INVESTOR' else None
    if role == 'INVESTOR' or role == 'PROVIDER':
        w = Wallet()
        user_data['wallet'] = {
            'owned_credits': [],
            'private_key': w.private_key,
            'public_key': w.public_key
        }

    if user_uuid:
        user_data['uuid'] = str(user_uuid)

    try:
        db.collection(collection).document(email).set(user_data)
    except Exception as e:
        print(e)

    return user_data


class AuthService:
    @staticmethod
    def sign_up(req: SignUpRequest):
        name = req.name
        email = req.email
        password = req.password
        role = req.role
        if email is None or password is None:
            return None
        try:
            user = auth.create_user(
                email=email,
                password=password
            )

            collection = 'Trader' if role == 'INVESTOR' else 'CreditProvider' if role == 'PROVIDER' else 'Auditors'

            response = add_user(name, email, role, collection)
            response['uid'] = user.uid

            return response
        except Exception as e:
            return e

    @staticmethod
    def get_user(email):
        credit_provider_user = db.collection('CreditProvider').document(email).get()
        if credit_provider_user.exists:
            return credit_provider_user.to_dict()

        investor_user = db.collection('Trader').document(email).get()
        if investor_user.exists:
            print(investor_user)
            return investor_user.to_dict()

        auditor_user = db.collection('Auditors').document(email).get()
        if auditor_user.exists:
            return auditor_user.to_dict()

        return None

    @staticmethod
    async def login(req):
        req_json = await req.json()
        email = req_json['email']
        password = req_json['password']
        try:
            user = pb.auth().sign_in_with_email_and_password(email, password)
            response = AuthService.get_user(email)

            if not response:
                raise Exception('Not found user')

            response['token'] = user['idToken']

            return response
        except Exception as e:
            return e

    @staticmethod
    async def remove_trader_account(email: str):
        found_trader = db.collection('Trader').document(email).get()

        if not found_trader.exists:
            raise Exception('Trader not found')

        db.collection('Trader').document(email).delete()
        user = auth.get_user_by_email(email)
        user_uid = user.uid

        auth.delete_user(user_uid)


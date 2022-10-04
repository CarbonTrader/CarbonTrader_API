import firebase_admin
from firebase_admin import firestore


cred_obj = firebase_admin.credentials.Certificate(
    "app/secrets/service_account_key.json")
default_app = firebase_admin.initialize_app(cred_obj)
db = firestore.client()

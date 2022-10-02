import stat
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./service_account_key.json')
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()


class RecoveryService:

    @staticmethod
    def get_blockchian():
        doc_ref = db.collection(u'Blockchain').document(u'Blockchain')
        doc = doc_ref.get()
        return doc.to_dict()

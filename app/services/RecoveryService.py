from re import I
from app.config.firebaseConfig import db
import time


class RecoveryService:

    @staticmethod
    def get_blockchain():
        docs = db.collection(u'Blockchain').stream()
        blockchain = []
        for doc in docs:
            blockchain.append(
                RecoveryService.re_order_block_values(doc.to_dict()))

        return blockchain

    @staticmethod
    def update_blockchain(blockchain):
        docs = db.collection(u'Blockchain').stream()
        for doc in docs:
            doc.reference.delete()

        name = "node0"
        for i in range(len(blockchain)):
            name = name[:-1] + str(i)
            print(name)
            db.collection(u'Blockchain').document(name).set(blockchain[i])

        return {"Message": "Blockchain updated."}

    @staticmethod
    def re_order_block_values(block):
        return {
            "timestamp": block.get("timestamp"),
            "last_hash": block.get("last_hash"),
            "hash": block.get("hash"),
            "merkle_root": block.get("merkle_root"),
            "number_transactions": block.get("number_transactions"),
            "transactions_hashes": block.get("transactions_hashes")
        }

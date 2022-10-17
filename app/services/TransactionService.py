import json
import logging
import os
import time
import uuid
from concurrent import futures

from google.cloud import pubsub_v1

from app.Model.Transaction import Transaction
from app.blockchain.Transaction import Transaction
from app.blockchain.Wallet import Wallet
from app.config.firebaseConfig import db
from app.services.UserService import UserService

"""
{
    "carbon_trader_serial":"carbon-trader-09-302-00",
    "recipient_email": "mario12@gmail.com",
    "sender_email":"e@example.com",
    "private_key_sender": "-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgyRdwdavTbmfBldZgylzU\nXyYxX5WPe+WAHmQaDkrXiOmhRANCAARawkffg+hxUcor68JsWX7/lW0YNs+rbp3b\nrE9TolBzgi77cVklf6qmTRwKeXUUqSU9FnnMm5mQiurtCimbzu50\n-----END PRIVATE KEY-----\n",
    "public_key_sender": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEWsJH34PocVHKK+vCbFl+/5VtGDbPq26d\n26xPU6JQc4Iu+3FZJX+qpk0cCnl1FKklPRZ5zJuZkIrq7Qopm87udA==\n-----END PUBLIC KEY-----\n"
}
"""

project_id = 'flash-ward-360216'
api_topic_id = 'vocero'
node_topic_subscription_id = 'nodes_info-sub'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "app/secrets/service-account-info.json"
# TODO: Change node list
# Se inicializa el publisher
publisher = pubsub_v1.PublisherClient()
api_topic_path = publisher.topic_path(project_id, api_topic_id)


def get_callback(future, message):
    def callback(future):
        try:
            logging.info("Published message %s.", future.result(timeout=1))
        except futures.TimeoutError as exc:
            print("Publishing %s timeout: %r", message, exc)

    return callback


def format_key(key: str):
    return key.replace("\\n", "\n")


def update_retire_date(transaction_type, serial, recipient_email, sender_email):
    print("entra")
    print(sender_email)
    found_cp = db.collection('CreditProvider').document(sender_email).get()

    if found_cp.exists:
        cp_projects = db.collection('CreditProvider').document(sender_email).collection('GreenProjects').stream()
        for project in cp_projects:
            project = project.to_dict()
            project_credits = project['credits']
            for credit in project_credits:
                if credit['carbontrader_serial'] == serial:
                    credit['retire_date'] = time.time_ns()
                    project['credits'] = project_credits
                    db.collection('CreditProvider').document(sender_email).collection('GreenProjects').document(
                        project['id']).set(project)


class TransactionService:

    @staticmethod
    def build_transaction(transaction_data):
        transaction_data['public_key_sender'] = format_key(transaction_data['public_key_sender'])
        transaction_data['private_key_sender'] = format_key(transaction_data['private_key_sender'])
        recipient_response = UserService.get_user(
            transaction_data["recipient_email"])
        sender_response = UserService.get_user(
            transaction_data["sender_email"])
        wallet = Wallet()
        wallet.upload_wallet(transaction_data["sender_email"], transaction_data["private_key_sender"],
                             transaction_data["public_key_sender"], [])

        trans = Transaction(str(uuid.uuid4()), transaction_data["type"], transaction_data.get(
            "carbon_trader_serial"), wallet, transaction_data.get("recipient_email"))

        TransactionService.transfer_credits(recipient_response, sender_response, transaction_data.get(
            "carbon_trader_serial"), trans.__dict__)
        return TransactionService.upload_transaction_to_blockchain(trans.__dict__)

    @staticmethod
    def transfer_credits(recipient_response, sender_response, serial, trans):
        recipient = recipient_response["response"]
        sender = sender_response["response"]
        recipient_credits = recipient.get("wallet").get("owned_credits")
        sender_credits = sender.get("wallet").get("owned_credits")
        sender_credits.remove(serial)
        recipient_credits.append(serial)
        sig = []
        sig.append(str(trans["signature"][0]))
        sig.append(str(trans["signature"][1]))
        trans["signature"] = sig

        db.collection(recipient_response["collection"]).document(recipient['email']).collection(
            'Transactions').document(
            trans['hash']).set(trans)
        db.collection(sender_response["collection"]).document(sender['email']).collection('Transactions').document(
            trans['hash']).set(trans)

        db.collection(u"Transaction").document(
            trans["hash"]).set(trans)
        db.collection(recipient_response["collection"]).document(
            recipient.get("email")).set(recipient)
        db.collection(sender_response["collection"]).document(
            sender.get("email")).set(sender)
        signature_aux = (int(trans["signature"][0]), int(trans["signature"][1]))
        trans["signature"] = signature_aux
        db.collection("Seriales_En_Venta").document(trans['carbon_trader_serial']).delete()
        update_retire_date(trans['transaction_type'], trans['carbon_trader_serial'], recipient['email'], sender['email'])

    @staticmethod
    def get_all_transactions():
        result_transactions = []
        trans = db.collection('Transaction').stream()
        for transaction in trans:
            transaction = transaction.to_dict()
            result_transactions.append(transaction)
        return result_transactions

    @staticmethod
    def upload_transaction_to_blockchain(transaction: Transaction):
        publish_futures = []
        data = {
            "type": 'api_message',
            "transactions": transaction,
            "idTransaction": transaction["id"],
        }

        message = json.dumps(data, ensure_ascii=False).encode('utf8')

        future1 = publisher.publish(api_topic_path, message)
        future1.add_done_callback(get_callback(future1, message))
        publish_futures.append(future1)

        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        return transaction

    @staticmethod
    def multi_exchange(request):
        print(request)
        found_cp = db.collection('CreditProvider').document(request['cp_email']).get()
        if not found_cp.exists:
            raise Exception('Not found Credit Provider')

        found_cp = found_cp.to_dict()

        cp_credits = found_cp['wallet']['owned_credits']
        selected_cp_credits = cp_credits[:request['amount']]

        for credit in selected_cp_credits:
            transaction = {
                'carbon_trader_serial': credit,
                'recipient_email': request['recipient_email'],
                'sender_email': request['cp_email'],
                'private_key_sender': request['private_key_sender'],
                'public_key_sender': request['public_key_sender'],
                'type': 'exchange'
            }

            TransactionService.build_transaction(transaction)

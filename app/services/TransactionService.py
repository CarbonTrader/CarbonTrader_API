from app.Model.Transaction import Transaction
import json
import os
import logging
from concurrent import futures
from google.cloud import pubsub_v1
import os
from app.blockchain.Wallet import Wallet
from app.config.firebaseConfig import db
import uuid
from app.blockchain.Transaction import Transaction
from app.services.UserService import UserService
import json

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
nodes_list = ['node1', 'node2', 'node3']
test_k = "-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgyRdwdavTbmfBldZgylzU\nXyYxX5WPe+WAHmQaDkrXiOmhRANCAARawkffg+hxUcor68JsWX7/lW0YNs+rbp3b\nrE9TolBzgi77cVklf6qmTRwKeXUUqSU9FnnMm5mQiurtCimbzu50\n-----END PRIVATE KEY-----\n"
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


class TransactionService:

    @staticmethod
    def build_transaction(transaction_data):
        recipient_response = UserService.get_user(
            transaction_data["recipient_email"])
        sender_response = UserService.get_user(
            transaction_data["sender_email"])

        wallet = Wallet()
        wallet.upload_wallet(transaction_data["sender_email"], transaction_data["private_key_sender"],
                             transaction_data["public_key_sender"], [])

        trans = Transaction(str(uuid.uuid4()), "exchange",  transaction_data.get(
            "carbon_trader_serial"), wallet, transaction_data.get("recipient_email"))

        TransactionService.transfer_credits(recipient_response, sender_response, transaction_data.get(
            "carbon_trader_serial"))
        return TransactionService.create_transaction(trans.__dict__)

    @staticmethod
    def transfer_credits(recipient_response, sender_response, serial):
        recipient = recipient_response["response"]
        sender = sender_response["response"]
        recipient_credits = recipient.get("wallet").get("owned_credits")
        sender_credits = sender.get("wallet").get("owned_credits")
        sender_credits.remove(serial)
        recipient_credits.append(serial)
        db.collection(recipient_response["collection"]).document(
            recipient.get("email")).set(recipient)
        db.collection(sender_response["collection"]).document(
            sender.get("email")).set(sender)

    @staticmethod
    def create_transaction(transaction: Transaction):
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

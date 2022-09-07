from app.Model.Blockchain import Blockchain
import json
import os
import logging
import threading
from concurrent import futures
from google.auth import jwt
from google.cloud import pubsub_v1
import os
from pydantic import BaseSettings

from app.blockchain.Transaction import Transaction


project_id = 'flash-ward-360216'
api_topic_id = 'vocero'
node_topic_subscription_id = 'nodes_info-sub'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "app/secrets/service-account-info.json"
# TODO: Change node list
nodes_list = ['node1', 'node2', 'node3']

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


def main(transaction: Transaction):

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

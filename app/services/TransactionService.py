from app.Model.Transaction import Transaction
import json
import os
import logging
from concurrent import futures
from google.cloud import pubsub_v1
import os
import threading
from app.blockchain.Transaction import Transaction


project_id = 'flash-ward-360216'
api_topic_id = 'vocero'
node_topic_subscription_id = 'nodes_info-sub'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "app/secrets/service-account-info.json"

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
    def __init__(self, api_subscriber, api_topic_subscription_path) -> None:
        self.api_subscriber = pubsub_v1.SubscriberClient()
        self.api_topic_subscription_path = api_subscriber.subscription_path(
            project_id, 'APIX')

    def test(self):
        try:
            with self.api_subscriber:
                self.api_subscriber.delete_subscription(
                    request={"subscription": self.api_topic_subscription_path})
        except:
            print("a")

    def handle_message(self, message):
        message_type = message['type']
        if message_type == 'response_audit':
            self.test()

    def create_subscription(subscriber, topic_sub_path, topic_path):
        subscriber.create_subscription(
            request={"name": topic_sub_path,
                     "topic": topic_path})

    def listener_transactions_messages(self):
        with self.api_subscriber:
            subscriptions = []
            for sub in self.api_subscriber.list_subscriptions(request={"project": 'projects/' + project_id}):
                subscriptions.append(sub.name)

            if self.api_topic_subscription_path in subscriptions:
                self.api_subscriber.delete_subscription(
                    request={"subscription": self.api_topic_subscription_path})

            self.create_subscription(
                self.api_subscriber, self.api_topic_subscription_path, api_topic_path)

            future = api_subscriber.subscribe(
                api_topic_subscription_path, callback=callback)
            try:
                future.result()
            except futures.TimeoutError:
                future.result()
                future.cancel()
                api_subscriber.delete_subscription(
                    request={"subscription": api_topic_subscription_path})

    def callback(message):
        try:
            message.ack()
            data = json.loads(message.data.decode('utf-8'))
            handle_message(data)
        except:
            print("ASD")

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

    @staticmethod
    def begin_audit(params: dict):
        print(params)
        data = {
            'type': 'audit',
            'parameters': {
                "audit_type": 1,
                "merkle_search": [[1, "4267438e03fee933fbc15fd74411c00575e11785773862e0751d74cf15efed1f"]]
            }
        }
        message_to_send = json.dumps(
            data, ensure_ascii=False).encode('utf8')
        future1 = publisher.publish(
            api_topic_path, message_to_send)
        future1.result()
        listener_transactions_messages()

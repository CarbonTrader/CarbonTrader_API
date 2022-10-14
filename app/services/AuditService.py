import json
from concurrent import futures
from google.cloud import pubsub_v1
import os
import time
from app.config.firebaseConfig import db
import threading
project_id = 'flash-ward-360216'
api_topic_id = 'vocero'
node_topic_subscription_id = 'nodes_info-sub'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "app/secrets/service-account-info.json"
import uuid
# Se inicializa el publisher



class AuditService:
    def __init__(self) -> None:
        self.api_subscriber = pubsub_v1.SubscriberClient()
        self.api_topic_subscription_path = self.api_subscriber.subscription_path(
            project_id, "APIS")
        self.publisher = pubsub_v1.PublisherClient()
        self.api_topic_path = self.publisher.topic_path(project_id, api_topic_id)

    @staticmethod
    def end_conection(api_subscriber,api_topic_subscription_path):
        with api_subscriber:
            api_subscriber.delete_subscription(
                request={"subscription": api_topic_subscription_path})

    def audit_topic_handler(self,message):
        print("asd")
        print(message)
        """basic_bitch = {
            "test1" : True,
            "Test2" : True,
            "Test3" : [True]
        }
        nodes = [basic_bitch for i in range(10)]
        node_id = "Node0"
        for i in range(1,len(nodes)+1):
            db.collection(u"Audit").document(node_id).set(nodes[i-1])
            node_id = node_id[:-1] + str(i)
        docs = db.collection(u'Audit').stream() 
        for doc in docs:
            nodes.append(doc.to_dict())"""


    def handle_message(self, message):
        message_type = message['type']
        if message_type == 'audit_response':
            self.audit_topic_handler(message)

    def create_subscription(self, subscriber, topic_sub_path, topic_path):
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
                self.api_subscriber, self.api_topic_subscription_path, self.api_topic_path)

            future = self.api_subscriber.subscribe(
                self.api_topic_subscription_path, callback=self.callback)
            try:
                future.result()
            except futures.TimeoutError:
                future.result()
                future.cancel()
                self.api_subscriber.delete_subscription(
                    request={"subscription": self.api_topic_subscription_path})

    def callback(self, message):
        message.ack()
        data = json.loads(message.data.decode('utf-8'))
        self.handle_message(data)

    def test(self):
        while True:
            print("Asd")
            time.sleep(0.5)


    def begin_audit(self, params: dict):
        message_to_send = json.dumps(
            params, ensure_ascii=False).encode('utf8')
        future1 = self.publisher.publish(
            self.api_topic_path, message_to_send)
        future1.result()
        thread1 = thread("GFG", 1000, self.api_subscriber,self.api_topic_subscription_path)
        thread1.start()
        self.listener_transactions_messages()


class thread(threading.Thread):
    def __init__(self, thread_name, thread_ID, api_subscriber, api_topic_subscription_path):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.api_subscriber = api_subscriber
        self.api_topic_subscription_path = api_topic_subscription_path

        # helper function to execute the threads

    def run(self):
        print(str(self.thread_name) + " " + str(self.thread_ID))
        time.sleep(15)
        AuditService.end_conection(self.api_subscriber, self.api_topic_subscription_path)

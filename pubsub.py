
"""Cloud Pub/Sub gRPC sample application."""

from __future__ import print_function

from google.pubsub.v1 import pubsub_pb2
from grpc.beta import implementations
from grpc.framework.interfaces.face.face import NetworkError
from oauth2client import client
from dotenv import load_dotenv
from uuid import uuid4

import logging,sys,json,base64,os,datetime

load_dotenv()

class Error(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
            self.data = args[1]
            self.pubsub = args[2] or False
        else:
            self.message = None
            self.data = ''
            self.pubsub = False
        
        print('Failed to publish message: {}'.format(self.data))

        publisher.publish_message(self.data, self.message,True) if self.pubsub else None

    def __str__(self) -> str:
        return self.message
class PubSub():

    def __init__(self,topic) -> None:
        self.PUBSUB_ENDPOINT = "pubsub.googleapis.com"
        self.SSL_PORT = 443
        self.OAUTH_SCOPE = "https://www.googleapis.com/auth/pubsub",
        self.GOOGLE_CREDS = client.GoogleCredentials.get_application_default()
        self.SCOPED_CREDS = self.GOOGLE_CREDS.create_scoped(self.OAUTH_SCOPE)
        self.TIMEOUT = 30
    
        self.ssl_creds = implementations.ssl_channel_credentials(None, None, None)
        self.stub = self.create_pubsub_stub()
        self.topic = topic

    def auth_func(self):
        """Returns a token obtained from Google Creds."""
        authn = self.SCOPED_CREDS.get_access_token().access_token
        return [('authorization', 'Bearer %s' % authn)]

    def make_channel_creds(self):
        """Returns a channel with credentials callback."""
        call_creds = implementations.metadata_call_credentials(
            lambda ctx, callback: callback(self.auth_func(), None))
        return implementations.composite_channel_credentials(self.ssl_creds, call_creds)

    def create_pubsub_stub(self) :
        """Creates a secure pubsub channel."""
        channel_creds = self.make_channel_creds()
        channel = implementations.secure_channel(self.PUBSUB_ENDPOINT, self.SSL_PORT, channel_creds)
        return pubsub_pb2.beta_create_Publisher_stub(channel)

    def publish_message(self,message,module,id_,error=False):
        """Publishes a message to a topic."""
        # req = pubsub_pb2.ListTopicsRequest(project=project)

        data_send = {
            "valor":message,
            "table": "table_erro" if error else module,
            "id":id_,
            "timestamp":str(datetime.datetime.now())
        }

        data = base64.b64encode(bytes(json.dumps(data_send),'utf-8'))

        message = pubsub_pb2.PubsubMessage(data=data)
        
        sub = pubsub_pb2.PublishRequest(topic=self.topic,messages =[message])

        try:
            # resp = stub.ListTopics(req, TIMEOUT)
            self.stub.Publish(sub,self.TIMEOUT)
            # for t in resp.topics:
            #     print("Topic is: {}".format(t.name))
        except NetworkError as e:
            Error('table_erro',str(e),True)
            pass

publisher = PubSub(os.getenv('TOPIC'))
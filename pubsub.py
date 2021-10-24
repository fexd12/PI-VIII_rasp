
"""Cloud Pub/Sub gRPC sample application."""

from __future__ import print_function

from google.pubsub.v1 import pubsub_pb2
from grpc.beta import implementations
from grpc.framework.interfaces.face.face import NetworkError
from oauth2client import client
from dotenv import load_dotenv

import logging,sys,json,base64

load_dotenv()

class PubSubError(Exception):
        
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
            self.data = base64.b64encode(bytes(args[1], 'utf-8'))
        else:
            self.message = None
            self.data = base64.b64encode(bytes({}, 'utf-8'))

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

    def publish_message(self,message,module,error):
        """Publishes a message to a topic."""
        # req = pubsub_pb2.ListTopicsRequest(project=project)
        data_send = {
            "tipo_sensor": module,
            "error": "X" if error else "",
            "valor":message
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
            print('Failed to publish message: {}'.format(e))
            raise PubSubError('PubSub',str(e.message))

publisher = PubSub('projects/southern-waters-328922/topics/Sensor')
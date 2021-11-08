import io,base64,requests,json,os

from pubsub import publisher 
from picamera import PiCamera

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

class CameraError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
            self.data = args[1]
        else:
            self.message = None
            self.data = {}
        
        publisher.publish_message(self.data, self.message,True)

    def __str__(self) -> str:
        return self.message

class Camera:
    def __init__(self):
        self.camera = PiCamera()

    def _take_picture(self):

        try:
            stream = io.BytesIO()

            for _ in self.camera.capture_continuous(stream,'jpeg'):
                    
                stream.seek(0)

                img_encoded = base64.b64encode(stream.read()).decode('utf-8')

                data = json.dumps({
                    'image': img_encoded
                })

                print('making request')
                # print(data)
                # res = requests.post('http://104.198.67.173:2000/separacao/',data=data)
                # print(res.json())

                stream.seek(0)
                stream.truncate()

                return data
        except Exception as e :
            CameraError('Camera',str(e.message))
            pass
    
    def detect(self):
        try:
            data = self._take_picture()
        
            prediction_client = automl_v1beta1.PredictionServiceClient()

            name = 'projects/{}/locations/us-central1/models/{}'.format(os.getenv('PROJECT'), os.getenv('MODEL_IA'))
            
            payload = {'image': {'image_bytes': data }}

            params = {}
            
            return prediction_client.predict(name, payload, params)
        
        except CameraError as e :
            # CameraError('Camera',str(e.message))
            pass


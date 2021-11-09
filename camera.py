import io,base64,requests,json,os

from pubsub import publisher 
from picamera import PiCamera

from google.cloud import automl_v1beta1

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

                stream.seek(0)
                stream.truncate()

                return img_encoded
        except Exception as e :
            CameraError('Camera',str(e.message))
            pass

    def detect(self):
        try:
            data = self._take_picture()
        
            prediction_client = automl_v1beta1.PredictionServiceClient()

            model_full_id = automl_v1beta1.AutoMlClient.model_path(
                os.getenv('PROJECT'), "us-central1", os.getenv('MODEL_IA'))

            image = automl_v1beta1.Image(image_bytes=data)

            payload = automl_v1beta1.ExamplePayload(image=image)

            request = automl_v1beta1.PredictRequest(name=model_full_id, payload=payload, params={})

            result = prediction_client.predict(request=request)
            print(result)
            
            # publisher.publish_message(result.payload.display_name, 'camera')
            
            return result

        except CameraError as e :
            # CameraError('Camera',str(e.message))
            pass

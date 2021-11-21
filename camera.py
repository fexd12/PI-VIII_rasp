import io,base64,requests,json

from pubsub import publisher 
from picamera import PiCamera
from google.cloud import vision


class CameraError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
            self.data = args[1]
        else:
            self.message = None
            self.data = ''
        
        publisher.publish_message(self.data, self.message,True)

    def __str__(self) -> str:
        return self.message

class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.image_annotator = vision.ImageAnnotatorClient()

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

                stream.seek(0)
                stream.truncate()

                return data
        except Exception as e :
            CameraError('erro',str(e.message))
            pass
    
    def crop_hints(self):

        try:
            data_image = self._take_picture()

            image = vision.Image(content=data_image['image'])

            crop_hints_params = vision.CropHintsParams(aspect_ratios=[1.77])

            image_context = vision.ImageContext(
                crop_hints_params=crop_hints_params)

            response = self.image_annotator.crop_hints(image=image, image_context=image_context)

            hints = response.crop_hints_annotation.crop_hints

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in hints[0].bounding_poly.vertices])

            return vertices
        except CameraError as e:
            raise e
    
    def image_properties(self):
        try:
            data_image = self._take_picture()

            image = vision.Image(content=data_image['image'])

            response = self.image_annotator.image_properties(image=image)
            props = response.image_properties_annotation

            return props

        except CameraError as e:
            raise e
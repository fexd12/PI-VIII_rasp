import io,base64,requests,json

from picamera import PiCamera
from google.cloud import vision

class CameraError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
            self.data = base64.b64encode(bytes(args[1], 'utf-8'))
        else:
            self.message = None
            self.data = base64.b64encode(bytes({}, 'utf-8'))

    def __str__(self) -> str:
        return self.message

class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.image_annotator = vision.ImageAnnotatorClient()

    def take_picture(self):

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
            raise CameraError('module Camera error',str(e.message))
    
    def crop_hints(self):

        try:
            data_image = self.take_picture()

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
            data_image = self.take_picture()

            image = vision.Image(content=data_image['image'])

            response = self.image_annotator.image_properties(image=image)
            props = response.image_properties_annotation

            return props

        except CameraError as e:
            raise e
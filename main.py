from threading import Thread
from dotenv import load_dotenv
from camera import Camera
from sensor import Sensor

load_dotenv()

def leitura_camera():
    camera = Camera()
    while True:
        camera.detect()

def leitura_sensor():
    sensor_1 = Sensor('','1')
    sensor_2 = Sensor('','2')
    sensor_3 = Sensor('','3')

    while True:
        sensor_1.read_sensor()
        sensor_2.read_sensor()  
        sensor_3.read_sensor()

def main():

    try:
        t_camera = Thread(target=leitura_camera,args=())
        t_camera.start()

        # t_sensor = Thread(target=leitura_sensor,args=())
        # t_sensor.start()

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
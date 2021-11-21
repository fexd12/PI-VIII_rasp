from pubsub import publisher
from utils import Pin,Error

class Sensor(Pin):
    def __init__(self,pin) -> None:
        Pin.__init__(self,pin)
        # self.sensor = Pin(pin)
        self.name = "infravermelho"
        
    def read_sensor(self):
        try:
            value, voltage = self.read_pin()
            print("{:>5}\t{:>5.3f}V".format(value, voltage))
            publisher.publish_message(value, self.name)

        except Exception as e :
            Error('erro',str(e.message))
            pass

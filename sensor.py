import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP

from pubsub import publisher
from adafruit_mcp3xxx.analog_in import AnalogIn

class SensorError(Exception):
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


class Pin():
    def __init__(self,pin) -> None:
        self.pin = pin

        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        self.cs = digitalio.DigitalInOut(board.D22)

        # create the mcp object
        self.mcp = MCP.MCP3008(self.spi, self.cs)

        # create an analog input channel on pin 0
    
    def read_pin(self):
        chan0 = AnalogIn(self.mcp, self.pin)
        return chan0.value, chan0.voltage

class Sensor(Pin):
    def __init__(self,pin,name) -> None:
        Pin.__init__(self,pin)
        # self.sensor = Pin(pin)
        self.name = f"""Sensor {name}"""
        
    def read_sensor(self):
        try:
            value, voltage = self.read_pin()
            print("{:>5}\t{:>5.3f} V".format(value, voltage))
            publisher.publish_message(value, self.name,False)

        except Exception as e :
            SensorError(self.name,str(e.message))
            pass
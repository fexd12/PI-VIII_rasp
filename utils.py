import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP

from pubsub import publisher
from adafruit_mcp3xxx.analog_in import AnalogIn

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

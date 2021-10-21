import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
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

class Sensor():
    def __init__(self,pin) -> None:
        self.sensor = Pin(pin)
        
    def read_sensor(self):
        pass
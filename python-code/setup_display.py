from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7735 as TFT
import Adafruit_GPIO.SPI as SPI

# Make the following 2 numbers bigger if you have multi-coloured pixels around the edge of the screen.
WIDTH = 128 # I used 130
HEIGHT = 160 # I used 161
SPEED_HZ = 4000000

# The pins of where we wired the DC and RES pins.
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Create a TFT screen object.
DISPLAY = TFT.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(
        SPI_PORT,
        SPI_DEVICE,
        max_speed_hz=SPEED_HZ),
    width=WIDTH,
    height=HEIGHT)

# Start up the display.
DISPLAY.begin()
DISPLAY.clear()
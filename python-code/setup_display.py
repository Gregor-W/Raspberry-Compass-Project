from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7735 as TFT
import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO.SPI as SPI
import numpy as np

# Make the following 2 numbers bigger if you have multi-coloured pixels around the edge of the screen.
WIDTH = 128 # I used 130
HEIGHT = 160 # I used 161
SPEED_HZ = 64000000

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
        SPI_DEVICE),
    width=WIDTH,
    height=HEIGHT,
    clock_hz=SPEED_HZ)

# Start up the display.
DISPLAY.begin()
DISPLAY.clear()

# fonts for Pillow
font = ImageFont.truetype("/home/pi/Raspberry-Compass-Project/python-code/OpenSans-Regular.ttf", 55)
font2 = ImageFont.truetype("/home/pi/Raspberry-Compass-Project/python-code/OpenSans-Regular.ttf", 30)
font3 = ImageFont.truetype("/home/pi/Raspberry-Compass-Project/python-code/OpenSans-Regular.ttf", 20)


# function for simple display
def display(heading, roll, pitch):
    # background
    image = Image.new("RGB", (HEIGHT, WIDTH), (0,0,0))
    
    # text
    draw = ImageDraw.Draw(image)

    draw.text((40, 0), "Heading", font=font3)
    draw.text((20, 12), "%.0f" % heading + chr(176), font=font)

    draw.text((110, 70), "Roll", font=font3)
    draw.text((86, 90), "%.0f" % roll + chr(176), font=font2)

    draw.text((5, 70), "Pitch", font=font3)
    draw.text((5, 90), "%.0f" % pitch + chr(176), font=font2)

    image = image.transpose(Image.ROTATE_90)
    DISPLAY.display(image)


# function for display with graphic compass
def fancy_display(heading, roll, pitch):
    # open images
    layer0 = Image.open("/home/pi/Raspberry-Compass-Project/python-code/graphics/Background.png")
    layer1 = Image.new("RGBA",(HEIGHT, WIDTH),(255,0,0,0))
    layer2 = Image.open("/home/pi/Raspberry-Compass-Project/python-code/graphics/Arrow.png")
    layer3 = Image.open("/home/pi/Raspberry-Compass-Project/python-code/graphics/Disc.png")

    # rotate compass
    layer3 = layer3.rotate(heading)
    
    # combine layers
    layer0.paste(layer3,(16,0),layer3.convert("RGBA"))
    layer0.paste(layer2,(0,0),layer2.convert("RGBA"))
    layer0 = layer0.transpose(Image.ROTATE_90)

    layer0 = Image.fromarray(np.array(layer0)[:, :, [2,1,0]])
    DISPLAY.display(layer0)

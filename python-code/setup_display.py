from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7735 as TFT
import Adafruit_GPIO.SPI as SPI
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
        SPI_DEVICE),
    width=WIDTH,
    height=HEIGHT)

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
    image = Image.new("RGB", (setup_display.HEIGHT, setup_display.WIDTH), (0,0,0))
    
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
    layer0 = Image.open("graphics/Background.png")
	layer1 = Image.new("RGBA",(setup_display.HEIGHT,setup_display.WIDTH),(255,0,0,0))
	layer2 = Image.open("graphics/Arrow.png")
	layer3 = Image.open("graphics/Disc.png")

	layer0.convert("RGBA")
	layer2.convert("RGBA")

	layer2 = layer2.transpose(Image.ROTATE_90)
	layer0 = Image.alpha_composite(layer1,layer2)

    # rotate compass
	layer3 = layer3.rotate(heading)
    
    # combine layers
	layer0.paste(layer3,(16,0),layer3.convert("RGBA"))
	layer0.paste(layer2,(0,0),layer2)
	layer0 = layer0.transpose(Image.ROTATE_90)
    
    DISPLAY.display(layer0)
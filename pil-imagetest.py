import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

WIDTH = 128
HEIGHT = 160

l_heading = 0
l_roll = 0
l_pitch = 0

font = ImageFont.truetype("python-code/OpenSans-Regular.ttf")

    

image = Image.new("RGB", (WIDTH, HEIGHT), (0,0,0))
draw = ImageDraw.Draw(image)


draw.text((10, 10), "H:" + str(l_heading), font=font)
draw.text((10, 20), "R:" + str(l_roll), font=font)
draw.text((10, 30), "P:" + str(l_pitch), font=font)


plt.imshow(image)
plt.show()



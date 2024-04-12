import os
from PIL import Image


def get_dominant_color(pil_img):
    img = pil_img.copy()
    img = img.convert("RGBA")
    img = img.resize((1, 1), resample=0)
    dominant_color = img.getpixel((0, 0))
    return dominant_color


IMAGESPATH = "./images/out"

for file in os.listdir(IMAGESPATH):
    img = Image.open(os.path.join(IMAGESPATH, file))
    color = (0, 0, 0, 255)
    while (color != (0, 0, 0, 255)): # Sometimes it bugs and give (0, 0, 0, 255) by default
        color = get_dominant_color(img)
    background = Image.new(size=(1170, 2532), color=color, mode="RGBA")

    img = img.resize((1170, 1170))
    background.paste(img, (0, 2532-1170-222))

    background.save("./images/out/processed/%s" % file)
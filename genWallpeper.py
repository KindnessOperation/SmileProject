import os
from PIL import Image
import threading

def get_dominant_color(pil_img):
    img = pil_img.copy()
    img = img.convert("RGBA")
    img = img.resize((1, 1), resample=0)
    dominant_color = img.getpixel((0, 0))
    return dominant_color

IMAGESPATH = "./images/out"
images = os.listdir(IMAGESPATH)

def task(i: int) -> None:
    if (i+1 == len(images)): return # Even number of images; Ignore last

    path1 = os.path.join(IMAGESPATH, images[i])
    path2 = os.path.join(IMAGESPATH, images[i+1])

    if (os.path.isdir(path1) or os.path.isdir(path2)): return

    img = Image.open(path1)
    img2 = Image.open(path2)

    background = Image.new(size=(1170, 2532), mode="RGBA")

    img = img.resize((1170, 1266))
    img2 = img2.resize((1170, 1266))


    background.paste(img, (0, 0))
    background.paste(img2, (0, 2532-1266))

    filename = "%s_%s" % (images[i].split(".")[0], images[i+1])
    background.save("./images/out/processed/%s" % filename)

threads: list[threading.Thread] = []
for i in range(0, len(images), 2):
    thread = threading.Thread(None, task, args=(i,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()    

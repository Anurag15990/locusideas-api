__author__ = 'anurag'


from app.settings import MEDIA_FOLDER
import base64
from PIL import Image
from flask import g
import datetime, random
import os


def save_image(base64String):
    if not os.path.exists(MEDIA_FOLDER):
        os.mkdir(MEDIA_FOLDER)

    file_content = base64.decodestring(base64String)
    path = "%s/%s.jpeg" %(MEDIA_FOLDER,  str(datetime.datetime.now()).split(' ')[0].replace('-', '') + "-" + str(random.randrange(9999999999999, 999999999999999999)))
    image = Image.frombytes('RGB', file_content)
    image.save(path)
    return path


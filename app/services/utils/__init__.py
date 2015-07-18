__author__ = 'anurag'


from app.settings import MEDIA_FOLDER
import base64
from PIL import Image
from flask import g
import datetime, random
import os



def decode_base64(data):
        missing_padding = 4 - len(data) % 4
        if missing_padding:
            data += b'='* missing_padding
        return base64.decodestring(data)


def save_image(base64String, image_path, image_thumbnail_path):
    size = 128, 128
    if not os.path.exists(MEDIA_FOLDER):
        os.mkdir(MEDIA_FOLDER)
    file_content = decode_base64(str(base64String))
    if image_path is None:
        name = str(datetime.datetime.now()).split(' ')[0].replace('-', '') + "-" + str(random.randrange(9999999999999, 999999999999999999))
        path = "%s/%s.jpg" %(MEDIA_FOLDER, name)
        file = open(path, "wb")
        file.write(file_content)
        thumbnail_path = "%s/%s-thumbnail.jpg" %(MEDIA_FOLDER, name)
        image = Image.open(path)
        image.thumbnail(size, Image.ADAPTIVE)
        image.save(thumbnail_path, "JPEG")
        file.close()
    else:
        path = image_path
        thumbnail_path = image_thumbnail_path
        file = open(path, "wb")
        file.truncate()
        file.write(file_content)
        if thumbnail_path is not None:
            image = Image.open(path)
            image.thumbnail(size, Image.ADAPTIVE)
            image.save(thumbnail_path, "JPEG")
        file.close()
    return path, thumbnail_path


def get_random():
    return random.randint(0, 999999999)



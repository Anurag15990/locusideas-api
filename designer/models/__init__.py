__author__ = 'anurag'

from designer.app import engine
import datetime
from designer.services.utils import get_random, decode_base64
from PIL import Image, ImageFile
import os, random, base64
from designer.settings import MEDIA_FOLDER


class ImageModel(engine.Document):

    image = engine.ImageField()
    image_path = engine.StringField()
    image_updated_time = engine.DateTimeField(default=datetime.datetime.now())
    thumbnail_path = engine.StringField()
    thumbnail_updated_time = engine.DateTimeField(default=datetime.datetime.now())
    icon_path = engine.StringField()
    icon_updated_time = engine.DateTimeField(default=datetime.datetime.now())

    meta = {
        "allow_inheritance" : True,
    }

def save_image(base64String):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    size = 300, 300
    icon_size = 64, 64
    if not os.path.exists(MEDIA_FOLDER):
        os.mkdir(MEDIA_FOLDER)
    file_content = decode_base64(str(base64String))
    name = str(datetime.datetime.now()).split(' ')[0].replace('-', '') + "-" + str(random.randrange(9999999999999, 999999999999999999))
    path = "%s/%s.jpg" %(MEDIA_FOLDER, name)
    file = open(path, "wb")
    file.write(file_content)
    thumbnail_path = "%s/%s-thumbnail.jpg" %(MEDIA_FOLDER, name)
    icon_path = "%s/%s-icon.jpg" %(MEDIA_FOLDER, name)
    image = Image.open(path)
    original_image = image
    image.thumbnail(size, Image.ADAPTIVE)
    image.save(thumbnail_path, "JPEG")
    image.thumbnail(icon_size, Image.ADAPTIVE)
    image.save(icon_path, "JPEG")
    file.close()
    return path, thumbnail_path, icon_path, path

class Node(object):

    title = engine.StringField()
    description = engine.StringField()
    created_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    updated_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    slug = engine.StringField()

    @classmethod
    def get_by_id(cls, id):
        return cls.objects(pk=id).first()

    @classmethod
    def get_by_slug(cls, slug):
        return cls.objects(slug__iexact=slug).first()


class Location(engine.Document):
    location = engine.StringField()
    geo_location = engine.PointField()
    city = engine.StringField()
    state = engine.StringField()
    country = engine.StringField()
    zipCode = engine.StringField()


class Charge(engine.Document):
    price = engine.DecimalField()
    currency = engine.StringField(choices=['INR', 'USD'])
    discount_percentage = engine.IntField()


    @property
    def actual_price(self):
        return self.price - (self.price * (self.discount_percentage / 100))


class Category(object):

    name = engine.StringField()
    description = engine.StringField()

class SubCategory(object):

    name = engine.StringField()
    category = engine.StringField()
    description = engine.StringField()
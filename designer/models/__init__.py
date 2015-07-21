__author__ = 'anurag'

from designer.app import engine
import datetime
from designer.services.utils import get_random, save_image


class ImageModel(engine.Document):

    image = engine.ImageField()
    image_path = engine.StringField()
    image_updated_time = engine.DateTimeField(default=datetime.datetime.now())
    thumbnail_path = engine.StringField()
    thumbnail_updated_time = engine.DateTimeField(default=datetime.datetime.now())
    icon_path = engine.StringField()
    icon_updated_time = engine.DateTimeField(default=datetime.datetime.now())

    @classmethod
    def create(cls, base64String):
       try:
        if not base64String:
               raise Exception("Cannot create Image")
        embedded_Image = ImageModel()
        embedded_Image.image_path, embedded_Image.thumbnail_path = save_image(base64String, image_path=None, image_thumbnail_path=None)
        embedded_Image.save()
        return embedded_Image
       except Exception,e:
           print e.message



class Node(object):

    title = engine.StringField()
    cover_image = engine.ReferenceField("ImageModel")
    description = engine.StringField()
    created_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    updated_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    slug = engine.StringField()
    image_gallery = engine.ListField(engine.ReferenceField("ImageModel"))

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
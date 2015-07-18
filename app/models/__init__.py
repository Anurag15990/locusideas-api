__author__ = 'anurag'

from app import engine, db
import datetime
from app.services.utils import get_random, save_image


class EmbeddedImageField(engine.Document):

    image_id = engine.IntField(default=get_random)
    image_path = engine.StringField()
    thumbnail_path = engine.StringField()

    @classmethod
    def create(cls, base64String):
       if not base64String:
           raise Exception("Cannot create Image")
       embedded_Image = EmbeddedImageField()
       embedded_Image.image_path, embedded_Image.thumbnail_path = save_image(base64String)
       embedded_Image.save()
       return embedded_Image

    @classmethod
    def update(cls, image_id, base64String):
        if EmbeddedImageField.objects(image_id=image_id).first() is None:
            raise Exception("No Image with id: ", image_id)
        else:
            document = EmbeddedImageField(image_id=image_id)
            document.image_path, document.thumbnail_path = save_image(base64String, document.image_path, document.thumbnail_path)
            document.save()
            return document


class Node(engine.Document):

    title = engine.StringField()
    cover_image_path = EmbeddedImageField()
    description = engine.StringField()
    created_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    updated_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    slug = engine.StringField()
    image_gallery = engine.ListField(EmbeddedImageField())

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
    discount_percentage = db.IntField()


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
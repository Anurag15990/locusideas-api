__author__ = 'anurag'

from app import engine, db
import datetime


class Node(engine.Document):

    title = engine.StringField()
    cover_Image = engine.ImageField(thumbnail_size=(128, 128))
    image_gallery = engine.ListField(engine.ImageField(thumbnail_size=(128,128)))
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



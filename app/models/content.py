__author__ = 'anurag'

from app.models import Node, Gallery, Charge, Category, SubCategory
from app import engine


class Design(Node, Gallery, Charge, engine.Document):

    user = engine.StringField()
    categories = engine.ListField(engine.StringField())
    sub_categories = engine.ListField(engine.StringField())

    @classmethod
    def create(cls, title, cover_Image, **kwargs):
        if not title:
            raise Exception('Title Required')

        design = Design(title=title, cover_Image=cover_Image)
        for k, v in kwargs:
            if hasattr(design, k):
                setattr(design, k, v)
        design.save()
        return design

    def update(self, key, value):
        setattr(self, key, value)
        return self

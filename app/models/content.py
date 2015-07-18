__author__ = 'anurag'

from app.models import Node,  Charge, Category, SubCategory
from app import engine


class Design(Node, Charge, engine.Document):

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


class DesignCategoryMap(engine.Document):

    category = engine.GenericReferenceField()
    sub_category = engine.GenericReferenceField()
    design = engine.GenericReferenceField()

    @classmethod
    def create_design_category_map(cls, category, sub_category, design):
        if DesignCategoryMap.objects(category=category, sub_category=sub_category,design=design).first() is None:
            categoryMap = DesignCategoryMap(category=category, sub_category=sub_category,design=design)
            categoryMap.save()
            return categoryMap

    @classmethod
    def remove_design_category_map(cls, category, sub_category, design):
        category_map = DesignCategoryMap(category=category, sub_category=sub_category, design=design).first()
        if category_map is not None:
            category_map.delete()
            print("Removed Category Map: ", category_map)


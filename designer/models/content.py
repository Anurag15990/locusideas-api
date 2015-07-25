__author__ = 'anurag'


from designer.app import engine
from designer.models.user import User
import datetime
from ago import human

class Creatives(engine.Document):

    title = engine.StringField()
    description = engine.StringField()
    owner = engine.ReferenceField('User')
    category = engine.ListField(engine.StringField())
    sub_category = engine.ListField(engine.StringField())
    created_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    updated_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    slug = engine.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes': [
            { 'fields': ['-updated_timestamp', 'owner'], 'unique': False, 'sparse' : False, 'types' : False}
        ]
    }

    @property
    def get_Title(self):
        return self.title

    @property
    def get_description(self):
        return self.description

    @property
    def get_Category(self):
        return self.category

    @property
    def get_SubCategory(self):
        return self.sub_category

    @property
    def created_time(self):
        return human(self.created_timestamp, precision=1)

    @property
    def updated_time(self):
        return human(self.updated_timestamp, precision=1)

    @property
    def get_Owner(self):
        return User.objects(pk=self.owner).first()


class Designs(Creatives):

    price = engine.DecimalField()
    currency = engine.StringField(choices=['INR', 'USD'])
    discount = engine.IntField()
    view_Count = engine.IntField()

    @property
    def actual_price(self):
        return self.price - (self.price * (self.discount_percentage / 100))

    @property
    def get_views(self):
        return self.view_Count

    @classmethod
    def create(cls, title, user, **kwargs):
        node = Designs(title=title, user=user)
        if kwargs != None:
            for k in kwargs:
                if hasattr(node, k):
                    setattr(node, k, kwargs.get(k))
        node.save()
        return node



class PortFolio(Creatives):

    view_Count = engine.IntField()
    likes = engine.IntField()
    tags = engine.ListField(engine.StringField())

    @property
    def get_views(self):
        return self.view_Count

    @property
    def get_likes(self):
        return self.likes

    @property
    def get_tags(self):
        tagList = []
        for tag in self.tags:
            tagList.append(tag)
        return tagList


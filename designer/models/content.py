__author__ = 'anurag'


from designer.app import engine
import datetime

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
        "allow_inheritance" : True
    }

class Designs(Creatives):

    price = engine.DecimalField()
    currency = engine.StringField(choices=['INR', 'USD'])
    discount = engine.IntField()

    @property
    def actual_price(self):
        return self.price - (self.price * (self.discount_percentage / 100))


__author__ = 'anurag'

from app import engine
from app.models import Node

class User(engine.Document):

    first_name = engine.StringField()
    last_name = engine.StringField()
    email = engine.StringField()
    password = engine.StringField()
    address = engine.StringField()
    phone_Number = engine.StringField()
    mobile = engine.StringField()
    profile_photo = engine.ImageField(thumbnail_size=(128, 128))
    cover_Image = engine.ImageField(thumbnail_size=(128, 128))

    meta = {
        'allow_inheritance' : True,
        'indexes' : [
            {'fields': ['first_name', 'last_name', 'email'], 'unique' : False, 'sparse': False, 'types': False}
        ],
    }

class MyWorks(Node, engine.Document):
    
    designer = engine.StringField()
    view_count = engine.IntField()


class Designers(User, engine.Document):

    bio = engine.StringField()
    myWorks = engine.ListField(MyWorks())
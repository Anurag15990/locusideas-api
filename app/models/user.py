__author__ = 'anurag'

from app import engine
from app.models import Node, Gallery

class User(Node, engine.Document):

    first_name = engine.StringField()
    last_name = engine.StringField()
    email = engine.StringField()
    password = engine.StringField()
    address = engine.StringField()
    phone_Number = engine.StringField()
    mobile = engine.StringField()
    profile_photo = engine.ImageField(thumbnail_size=(128, 128))
    isAdmin = engine.BooleanField()
    isModerator = engine.BooleanField()

    meta = {
        'allow_inheritance' : True,
        'indexes' : [
            {'fields': ['first_name', 'last_name', 'email'], 'unique' : False, 'sparse': False, 'types': False}
        ],
    }




class MyWork(Node, Gallery, engine.Document):

    designer = engine.StringField()
    view_count = engine.IntField()



class Designer(User, engine.Document):

    institution = engine.StringField()
    experience = engine.StringField()
    proficiency = engine.StringField()
    bio = engine.StringField()
    myWorks = engine.ListField(MyWork())



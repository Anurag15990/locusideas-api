__author__ = 'anurag'

from app import engine
from app.models import Node, Gallery
import datetime, hashlib
from ago import human

class User(Node, engine.Document):

    first_name = engine.StringField()
    last_name = engine.StringField()
    email = engine.StringField()
    password = engine.StringField()
    address = engine.StringField()
    phone_Number = engine.StringField()
    mobile = engine.StringField()
    profile_photo = engine.ImageField(thumbnail_size=(128, 128))
    roles = engine.ListField(engine.StringField(('Basic User', 'Basic User'), ('Admin', 'Admin'), ('Moderator', 'Moderator') , ('Designer', 'Designer')))
    is_verified = engine.BooleanField()
    admin_approved = engine.BooleanField()
    user_since = engine.DateTimeField(default=datetime.datetime.now())
    last_login = engine.DateTimeField()

    meta = {
        'allow_inheritance' : True,
        'indexes' : [
            {'fields': ['first_name', 'last_name', 'email'], 'unique' : False, 'sparse': False, 'types': False}
        ],
    }

    @property
    def is_admin_approved_profile(self):
        if hasattr(self, 'admin_approved') and self.admin_approved:
            return True
        return False

    @property
    def since(self):
        return human(self.user_since, precision=1)

    @property
    def password(self):
        return self.password

    def __repr__(self):
        return self.title if self.title else (self.email if self.email else 'No name or email')


    def setTitle(self):
        if self.first_name:
            self.title += self.first_name
        if self.last_name:
            self.title += self.last_name
        self.save()
        return self.title

    @password.setter
    def password(self, new_val):
        self.password = hashlib.md5(new_val).hexdigest()

    def change_password(self, **kwargs):
        if kwargs['confirm'] == kwargs['password']:
            self.password = hashlib.md5(kwargs['password']).hexdigest()
            self.save()
        else:
            raise Exception('Passwords do not match')

    @classmethod
    def create(cls, name, email, **kwargs):
        user = User(name=name, email=email)
        for k, v in kwargs:
            if hasattr(user, k):
                setattr(user, k, v)
        user.save()
        return user

    def update(self, key, value):
        setattr(self, key, value)
        self.save()
        return self

    @classmethod
    def authenticate(cls, email, password):
        if password is None or len(password) is 0:
            return False
        user = User.objects(email__iexact=email).first()
        if user and user.password == hashlib.md5(password).hexdigest():
            if user.user_since is None:
                user.user_since = datetime.datetime.now()
                user.save()
                return user
        else:
            return False

    def update_last_login(self):
        self.last_login = datetime.datetime.now()


class MyWork(Node, Gallery, engine.Document):

    designer = engine.StringField()
    view_count = engine.IntField()

    @property
    def get_designer(self):
        return self.designer if self.designer else ('No Designer Linked')

    @property
    def get_view_count(self):
        if self.view_count:
            return self.view_count
        else:
            return 0

    @classmethod
    def create(cls, title, **kwargs):
        if not title:
            raise Exception('Title required')
        myWork = MyWork(title=title)
        for k, v in kwargs:
            if hasattr(myWork, k):
                setattr(myWork, k , v)
        myWork.save()
        return myWork

    def update(self, key, value):
        setattr(self, key, value)
        return self

class Designer(Node, engine.Document):

    user = engine.StringField()
    institution = engine.StringField()
    experience = engine.StringField()
    proficiency = engine.StringField()
    bio = engine.StringField()
    myWorks = engine.ListField(engine.StringField())


    @classmethod
    def create(cls, user, **kwargs):
        if not user:
            raise Exception('User is required')
        designer = Designer(user=user)
        for(k, v) in kwargs:
            if hasattr(designer, k):
                setattr(designer, k)
        designer.save()
        return designer

    @property
    def get_institution(self):
        if self.institution:
            return self.institution

    @property
    def get_experience(self):
        if self.experience:
            return self.experience

    @property
    def get_proficiency(self):
        if self.proficiency:
            return self.proficiency

    @property
    def get_bio(self):
        if self.bio:
            return self.bio

    @property
    def get_myWorks(self):
        if self.myWorks and len(self.myWorks) is not 0:
            return self.myWorks




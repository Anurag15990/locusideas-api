__author__ = 'anurag'

from designer.app import engine
from designer.models import Node
import datetime, hashlib
from ago import human

class User(Node, engine.Document):

    name = engine.StringField()
    email = engine.StringField()
    password = engine.StringField()
    address = engine.StringField()
    phone = engine.StringField()
    mobile = engine.StringField()
    roles = engine.ListField(engine.StringField())
    is_verified = engine.BooleanField()
    admin_approved = engine.BooleanField()
    user_since = engine.DateTimeField(default=datetime.datetime.now())
    last_login = engine.DateTimeField()
    institution = engine.StringField()
    experience = engine.StringField()
    proficiency = engine.StringField()
    bio = engine.StringField()

    meta = {
        'allow_inheritance' : True,
        'indexes' : [
            {'fields': ['name', 'email'], 'unique' : False, 'sparse': False, 'types': False}
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
    def passwd(self):
        return self.password

    def __repr__(self):
        return self.title if self.title else (self.email if self.email else 'No name or email')


    def setTitle(self):
        if self.name:
            self.title += self.name
        self.save()
        return self.title

    # @password.setter
    # def password(self, new_val):
    #     self.password = hashlib.md5(new_val).hexdigest()

    def change_password(self, **kwargs):
        if kwargs['confirm'] == kwargs['password']:
            self.password = hashlib.md5(kwargs['password']).hexdigest()
            self.save()
        else:
            raise Exception('Passwords do not match')

    @classmethod
    def create(cls, name, email, **kwargs):
        try:
            user = User(name=name, email=email)
            if kwargs != None:
                for k in kwargs:
                    if hasattr(user, k):
                        setattr(user, k, kwargs.get(k))
            user.save()
            return user
        except Exception, e:
            raise e

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
    def get_cover_image(self):
        from designer.models.image import UserImage
        return UserImage.objects(user=self, is_Current_Cover=True).first()

    @property
    def get_profile_image(self):
        from designer.models.image import UserImage
        return UserImage.objects(user=self, is_Current_Profile=True).first()
    




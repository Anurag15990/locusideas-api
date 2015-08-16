__author__ = 'anurag'

from designer.app import engine
from designer.models import Node, update_content
import datetime, hashlib, random
from ago import human


class Verification(engine.EmbeddedDocument):
    verification_link = engine.StringField()
    expiration = engine.DateTimeField()

    @classmethod
    def create_verification_link(self, user):
        v = Verification()
        v.verification_link = "/email-verification/%s/%s" % (str(user.id), str(hashlib.md5(str(random.randrange(000000000, 1000000000))).hexdigest()))
        v.expiration = datetime.datetime.now() + datetime.timedelta(days=2)
        return v

    def is_expired(self):
        return self.expiration <= datetime.datetime.now()

    def match(self, id, linkr):
        val = '/email-verification/%s/%s' % (id, linkr)
        print self.verification_link
        print val
        return self.verification_link == val

@update_content.apply
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
    work_focus = engine.ListField()
    work_interest = engine.ListField()
    work_style = engine.ListField()
    deactivated = engine.BooleanField(default=False)
    user_since = engine.DateTimeField(default=datetime.datetime.now())
    last_login = engine.DateTimeField()
    institution = engine.StringField()
    experience = engine.StringField()
    proficiency = engine.StringField()
    bio = engine.StringField()

    meta = {
        'indexes' : [
            {'fields': ['name', 'email'], 'unique' : False, 'sparse': False, 'types': False}
        ],
    }

    def create_verification_link(self):
        self.verification = Verification.create_verification_link(self)
        self.save()
        return self.verification.verification_link

    @classmethod
    def verify_user(cls, id, linkr):
        user = User.objects(pk=id).first()
        if user.is_verified:
            return True
        if user.verification.is_expired() :
            return False
        elif not user.verification.match(id, linkr):
            return False
        else:
            user.is_verified = True
            user.save()
            return user

    @property
    def is_admin(self):
        if not self.roles or len(self.roles) is 0:
            return False
        return 'Admin' in self.roles

    @property
    def is_designer(self):
        if not self.roles or len(self.roles) is 0:
            return False
        return 'Designer' in self.roles

    @property
    def is_admin_approved(self):
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


    def change_password(self, **kwargs):
        if kwargs.get('confirm') == kwargs.get('password'):
            self.password = hashlib.md5(kwargs.get('password')).hexdigest()
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

    # @property
    # def get_cover_image(self):
    #     from designer.models.image import UserImage
    #     image = UserImage.objects(user=self.id, is_Current_Cover=True).first()
    #     return image
    #
    # @property
    # def get_profile_image(self):
    #     from designer.models.image import UserImage
    #     return UserImage.objects(user=self.pk, is_Current_Profile=True).first()
    #


    @property
    def get_work_focus(self):
        if self.is_admin or (self.is_designer and self.is_admin_approved):
            if self.work_focus is not None:
                return self.work_focus
        else:
            return None

    @property
    def get_work_interest(self):
        if self.is_admin or (self.is_designer and self.is_admin_approved):
            if self.work_interest is not None:
                return self.work_interest
        else:
            return None

    @property
    def get_work_style(self):
        if self.is_admin or (self.is_designer and self.is_admin_approved):
            if self.work_style is not None:
                return self.work_style
        else:
            return None

    def deactivate(self):
        self.deactivated = True
        self.save()





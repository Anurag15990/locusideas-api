__author__ = 'anurag'

from designer.app import engine
import datetime
from designer.services.utils import get_random, decode_base64
from PIL import Image, ImageFile
import os, random, base64
from designer.settings import MEDIA_FOLDER


class ImageModel(object):

    image = engine.ImageField()
    image_path = engine.StringField()
    image_updated_time = engine.DateTimeField(default=datetime.datetime.now())
    thumbnail_path = engine.StringField()
    thumbnail_updated_time = engine.DateTimeField(default=datetime.datetime.now())
    icon_path = engine.StringField()
    icon_updated_time = engine.DateTimeField(default=datetime.datetime.now())

    def save_image(self, base64String):
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        size = 300, 300
        icon_size = 64, 64
        if not os.path.exists(MEDIA_FOLDER):
            os.mkdir(MEDIA_FOLDER)
        file_content = decode_base64(str(base64String))

        name = str(datetime.datetime.now()).split(' ')[0].replace('-', '') + "-" + str(random.randrange(9999999999999, 999999999999999999))
        path = "%s/%s.jpg" %(MEDIA_FOLDER, name)
        file = open(path, "wb")
        file.write(file_content)
        thumbnail_path = "%s/%s-thumbnail.jpg" %(MEDIA_FOLDER, name)
        icon_path = "%s/%s-icon.jpg" %(MEDIA_FOLDER, name)
        image = Image.open(path)
        image.thumbnail(size, Image.ADAPTIVE)
        image.save(thumbnail_path, "JPEG")
        image.thumbnail(icon_size, Image.ADAPTIVE)
        image.save(icon_path, "JPEG")
        file.close()
        return path, thumbnail_path, icon_path, image

class UserImage(ImageModel, engine.Document):

    user = engine.ReferenceField('User')
    type = engine.ListField(engine.StringField(choices=['Cover', 'Profile', 'Gallery']))
    is_Current_Cover = engine.BooleanField()
    is_Current_Profile = engine.BooleanField()

    @classmethod
    def create(cls, data, user):
        try:
            if not data:
                raise Exception("Cannot create Image")
            image = UserImage(user=user)
            image.image_path, image.thumbnail_path, image.icon_path, image.image = cls.save_image(cls, data['image'])
            if data['types'] is not None:
                for type in data['types']:
                    image.type.add(type)
            image.save()
            return image
        except Exception, e:
            raise e

    @classmethod
    def set_Cover(cls, image, user):
        if UserImage(image=image, user=user) is None:
            raise Exception("Image does not exist")
        image = UserImage(image=image,user=user)
        if image.is_Current_Cover is True:
            print('Already Current Cover')
        else:
            image.is_Current_Cover = True
            previous_Image = UserImage(user=user, is_Current_Cover=True)
            previous_Image.is_Current_Cover = False
            previous_Image.save()
            image.save()
            return image

    @classmethod
    def set_Profile(cls, image, user):
        if UserImage(image=image, user=user) is None:
            raise Exception("Image does not exist")
        image = UserImage(image=image,user=user)
        if image.is_Current_Profile is True:
            print("Already Current Profile Image")
        else:
            image.is_Current_Profile = True
            previous_Image = UserImage(user=user, is_Current_Profile=True)
            previous_Image.is_Current_Profile = False
            previous_Image.save()
            image.save()
            return image


class ContentImage(ImageModel, engine.Document):

    content = engine.ReferenceField('Content')
    type = engine.ListField(engine.StringField())
    is_Current_Cover = engine.BooleanField()

    @classmethod
    def create(cls, data, content):
        try:
            if not data:
                raise Exception("Cannot create Image")
            image = ContentImage(content=content)
            image.image_path, image.thumbnail_path, image.icon_path, image.image = cls.save_image(cls, data['image'])
            if data['types'] is not None:
                for type in data['types']:
                    image.type.add(type)
            image.save()
            return image
        except Exception, e:
            raise e

    @classmethod
    def set_Cover(cls, image, content):
        if ContentImage(image=image, content=content) is None:
            raise Exception("Image does not exist")
        image = UserImage(image=image, content=content)
        if image.is_Current_Cover is True:
            print('Already Current Cover')
        else:
            image.is_Current_Cover = True
            previous_Image = UserImage(content=content, is_Current_Cover=True)
            previous_Image.is_Current_Cover = False
            previous_Image.save()
            image.save()
            return image
        


class Node(object):

    title = engine.StringField()
    cover_image = engine.ReferenceField("ImageModel")
    description = engine.StringField()
    created_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    updated_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    slug = engine.StringField()
    image_gallery = engine.ListField(engine.ReferenceField("ImageModel"))

    @classmethod
    def get_by_id(cls, id):
        return cls.objects(pk=id).first()

    @classmethod
    def get_by_slug(cls, slug):
        return cls.objects(slug__iexact=slug).first()


class Location(engine.Document):
    location = engine.StringField()
    geo_location = engine.PointField()
    city = engine.StringField()
    state = engine.StringField()
    country = engine.StringField()
    zipCode = engine.StringField()


class Charge(engine.Document):
    price = engine.DecimalField()
    currency = engine.StringField(choices=['INR', 'USD'])
    discount_percentage = engine.IntField()


    @property
    def actual_price(self):
        return self.price - (self.price * (self.discount_percentage / 100))


class Category(object):

    name = engine.StringField()
    description = engine.StringField()

class SubCategory(object):

    name = engine.StringField()
    category = engine.StringField()
    description = engine.StringField()
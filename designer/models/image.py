__author__ = 'anurag'

from designer.models import ImageModel, save_image
from designer.models.user import User
from designer.models.creatives import Creatives
from designer.app import engine

class UserImage(ImageModel, engine.Document):

    user = engine.ReferenceField('User')
    is_Current_Cover = engine.BooleanField()
    is_Current_Profile = engine.BooleanField()

    @classmethod
    def create(cls, data, user):
        try:
            if not data:
                raise Exception("Cannot create Image")
            image = UserImage()
            image.image_path, image.thumbnail_path, image.icon_path, path = save_image(data['image'])
            image.image = open(path, "rb")
            image.user = User(pk=user)
            image.save()
            return image
        except Exception, e:
            raise e

    @classmethod
    def set_Cover(cls, image, user):
        if UserImage(pk=image, user=user) is None:
            raise Exception("Image does not exist")
        image = UserImage(pk=image,user=user)
        if image.is_Current_Cover is True:
            print('Already Current Cover')
        else:
            if UserImage.objects(user=user, is_Current_Cover=True).first() is not None:
                previous_Image = UserImage.objects(user=user, is_Current_Cover=True).first()
                previous_Image.modify(upsert=True, is_Current_Cover=False)
            image.is_Current_Cover = True
            image.modify(upsert=True, is_Current_Cover=True)
            return image

    @classmethod
    def set_Profile(cls, image, user):
        if UserImage(pk=image, user=user) is None:
            raise Exception("Image does not exist")
        image = UserImage(pk=image,user=user)
        if image.is_Current_Profile is True:
            print("Already Current Profile Image")
        else:
            if UserImage.objects(user=user, is_Current_Profile=True).first() is not None:
                previous_Image = UserImage.objects(user=user, is_Current_Profile=True).first()
                previous_Image.modify(upsert=True, is_Current_Profile=False)
            image.modify(upsert=True, is_Current_Profile=True)
            return image


class CreativesImage(ImageModel, engine.Document):

    creative = engine.ReferenceField('Creatives')
    is_Current_Cover = engine.BooleanField()
    caption = engine.StringField()

    @classmethod
    def create(cls, data, creative):
        try:
            if not data:
                raise Exception("Cannot create Image")
            image = CreativesImage()
            image.image_path, image.thumbnail_path, image.icon_path, path = save_image(data['image'])
            image.image = open(path, 'rb')
            image.creative = Creatives(creative)
            image.save()
            return image
        except Exception, e:
            raise e

    @classmethod
    def set_Cover(cls, image, creative):
        if CreativesImage(pk=image, creative=creative) is None:
            raise Exception("Image does not exist")
        image = CreativesImage(pk=image, creative=creative)
        if image.is_Current_Cover is True:
            print('Already Current Cover')
        else:
            if CreativesImage.objects(creative=creative, is_Current_Cover=True) is not None:
                previous_Image = UserImage(creative=creative, is_Current_Cover=True)
                previous_Image.modify(upsert=True, is_Current_Cover=False)
            image.modify(upsert=True, is_Current_Cover=True)
            return image


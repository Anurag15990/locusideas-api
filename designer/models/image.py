__author__ = 'anurag'

from designer.models import ImageModel, save_image
from designer.models.user import User
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


class ContentImage(ImageModel, engine.Document):

    content = engine.ReferenceField('Content')
    is_Current_Cover = engine.BooleanField()
    caption = engine.StringField()

    @classmethod
    def create(cls, data, content):
        try:
            if not data:
                raise Exception("Cannot create Image")
            image = ContentImage()
            image.image_path, image.thumbnail_path, image.icon_path, image.image = save_image(data['image'])
            image.save()
            return image
        except Exception, e:
            raise e

    @classmethod
    def set_Cover(cls, image, content):
        if ContentImage(pk=image, content=content) is None:
            raise Exception("Image does not exist")
        image = UserImage(pk=image, content=content)
        if image.is_Current_Cover is True:
            print('Already Current Cover')
        else:
            image.is_Current_Cover = True
            previous_Image = UserImage(content=content, is_Current_Cover=True)
            previous_Image.is_Current_Cover = False
            previous_Image.save()
            image.save()
            return image


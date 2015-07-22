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
            image.image_path, image.thumbnail_path, image.icon_path, image.upload_image = save_image(data['image'])
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
            image.is_Current_Cover = True
            previous_Image = UserImage(user=user, is_Current_Cover=True)
            previous_Image.is_Current_Cover = False
            previous_Image.save()
            image.save()
            return image

    @classmethod
    def set_Profile(cls, image, user):
        if UserImage(pk=image, user=user) is None:
            raise Exception("Image does not exist")
        image = UserImage(pk=image,user=user)
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
    is_Current_Cover = engine.BooleanField()

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


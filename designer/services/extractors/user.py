__author__ = 'anurag'

from designer.services.extractors.base import BaseExtractor
from bson import ObjectId


class UserExtractor(object):


    @classmethod
    def get_by_id(cls, id):
        from designer.models.user import User
        assert isinstance(id, str) or isinstance(id, unicode) or isinstance(id, ObjectId)
        return User.objects(pk=id).first()

    @classmethod
    def get_by_slug(cls, slug):
        from designer.models.user import User
        return BaseExtractor.get_by_slug(User, slug)




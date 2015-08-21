__author__ = 'anurag'

from designer.services.extractors.base import BaseExtractor
from designer.models.user import User
from designer.models.image import UserImage
from designer.services.utils import convert_filters_to_query
import json
from bson import ObjectId
from designer.services.utils import JSONSetEncoder
from designer.services.utils import login_required, setup_context


class UserExtractor(object):

    @classmethod
    def get_by_id(cls, id):
        assert isinstance(id, str) or isinstance(id, unicode) or isinstance(id, ObjectId)
        return User.objects(pk=id).first()

    @classmethod
    def get_by_slug(cls, slug):
        return BaseExtractor.get_by_slug(User, slug)




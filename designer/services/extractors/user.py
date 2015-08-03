__author__ = 'anurag'

from designer.services.extractors.base import BaseExtractor
from designer.models.user import User
from designer.models.image import UserImage
from designer.services.utils import convert_filters_to_query
import json
from designer.services.utils import JSONSetEncoder

class UserExtractor(BaseExtractor):

    def _invoke(self):
        response_Array = []
        if self.filters is not None or len(self.filters) > 0:
            query = convert_filters_to_query(filters=self.filters)
            users = User.objects(__raw__=query).all()
            facets = self.getFacets(users)
            for user in users:
                response_Array.append(self.getCard(user))
            return dict(status='success', users=response_Array, facets=facets)
        else:
            users = User.objects().all()
            facets = self.getFacets(users)
            for user in users:
                response_Array.append(self.getCard(user))
            return dict(status='success', users=response_Array, facets=facets)

    def getCard(self, user):
        userObject = {}
        userObject["id"] = str(user.id)
        if user.name is not None:
            userObject["name"] = user.name
        if user.email is not None:
            userObject["email"] = user.email
        if user.phone is not None:
            userObject["phone"] = user.phone
        if user.mobile is not None:
            userObject["mobile"] = user.mobile
        if user.address is not None:
            userObject["address"] = user.address
        if user.since is not None:
            userObject["userSince"] = user.since
        if self.getCover(str(user.id)) is not None:
            userObject["cover_Image"] = self.getCover(str(user.id))
        if self.getProfileImage(str(user.id)) is not None:
            userObject["profile_photo"] = self.getProfileImage(str(user.id))
        if user.is_designer == True:
            profileObject = {}
            if user.get_work_style is not None:
                profileObject["workStyle"] = user.get_work_style
            if user.get_work_focus is not None:
                profileObject["workFocus"] = user.get_work_focus
            if user.get_work_interest is not None:
                profileObject["workInterest"] = user.get_work_interest
            userObject['DesignerProfile'] = profileObject
        return userObject

    def getCover(self, user):
        cover = UserImage.objects(user=user, is_Current_Cover=True).first()
        if cover is not None:
            return cover

    def getProfileImage(self, user):
        profile_photo = UserImage.objects(user=user, is_Current_Profile=True).first()
        if profile_photo is not None:
          return profile_photo

    def getFacets(self, users):
        facets = {}
        interest_list = set([])
        focus_list = set([])
        style_list = set([])
        for user in users:
            if user.get_work_interest is not None:
                for interest in user.get_work_interest:
                    interest_list.add(interest)
            if user.get_work_focus is not None:
                for focus in user.get_work_focus:
                    focus_list.add(str(focus))
            if user.get_work_style is not None:
                for style in user.get_work_style:
                    style_list.add(str(style))
        facets["Work Styles"] = style_list
        facets["Work Focus"] = focus_list
        facets["Work Interest"] = interest_list
        return json.dumps(facets,cls=JSONSetEncoder)






__author__ = 'anurag'

from designer.services.editors.base import BaseEditor
from designer.models.user import User
from designer.models.image import UserImage
import zope

class UserEditor(BaseEditor):

    def _invoke(self):
        if self.command == 'edit-profile':
            response = edit_profile(self.node, self.data)
        elif self.command == 'register':
            response = register(self.data)
        elif self.command == 'edit-role':
            response = edit_role(self.action, self.node, self.message['role'])
        elif self.command == "update-cover":
            response = update_cover_photo(self.node, self.data)
        elif self.command == 'update-profile-photo':
            response = update_profile_photo(self.node, self.data)
        elif self.command == 'update-bio':
            response = update_bio(self.node, self.data)
        elif self.command == 'update-institution':
            response = update_institution(self.node, self.data)
        return response


def edit_profile(user, data):
    node = User(pk=user)
    for k, v in data.iteritems():
        if not hasattr(node, k) or k == 'email':
            continue
        v = v.strip()
        setattr(node, k, v)
        print("K[%s] : V[%s]" %(k,v))
    node.save()
    return node

def register(data):
    email, password, confirm, roles = data['email'], data['password'], data["confirm"], data['roles']
    if User.objects(email__iexact=email).first() is not None:
        raise Exception('User already exists')

    user = User.objects(email__iexact=email).first()
    if not user:
        user = User.create(name=data['name'], email=data['email'])
        if data['roles'] is None:
            user.roles = ['Basic User']
        else:
            user.roles = data['roles']
    try:
        user.change_password(confirm=confirm, password=password)

        if data['address'] is not None:
            user.address = data['address']

        if data['phone'] is not None:
            user.phone = data['phone']

        if data['mobile'] is not None:
            user.mobile = data['mobile']

        user.is_verified = False
        user.admin_approved = False

        user.save()
    except Exception,e:
        raise Exception(e)
    return user

def edit_role(action, user, role):
    node = User(pk=user)
    if action == "add":
        node.roles.append(role)
    elif action == "remove":
        node.roles.remove(role)
    else:
        print "Invalid Action"
    node.save()
    return node

def update_cover_photo(user, data):
    node = User(pk=user)
    if data['cover_image'] is not None:
        cover_image = data['cover_image']
        cover_Image = UserImage.set_Cover(cover_image, user=user)
    return cover_Image

def update_profile_photo(user, data):
    node = User(pk=user)
    if data['profile_photo'] is not None:
        profile_photo = data['profile_photo']
        profile_image = UserImage.set_Profile(profile_photo, user=user)
    return profile_image

def update_bio(user, data):
    node = User(pk=user)
    if data['bio'] is not None:
        node.bio = data['bio']
        node.save()
    return node

def update_institution(user, data):
    node = User(pk=user)
    if data['institution'] is not None:
        node.institution = data['institution']
        node.save()
    return node

def update_experience(user, data):
    node = User(pk=user)
    if data['experience'] is None:
        node.experience = data['Experience']
        node.save()
    return node
